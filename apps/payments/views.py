from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import json
import uuid
import logging

from apps.orders.models import Order
from .models import Payment, WalletTransaction, PaymentWebhook
# FIXED: Changed from campay_services to campay_service (singular)
from .services.campay_services import campay_service, CamPayError

logger = logging.getLogger(__name__)


@login_required
def payment_page(request, order_id):
    """Display payment page"""
    order = get_object_or_404(Order, id=order_id, employee=request.user)
    
    logger.info(f"Payment page accessed for order {order.order_number}, status: {order.status}")
    
    # Check if order can be paid
    if order.status not in [Order.STATUS_VALIDATED, Order.STATUS_PENDING]:
        messages.error(request, f'Order cannot be paid. Current status: {order.status}')
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'user': request.user
    }
    return render(request, 'employee/proceed_to_payment.html', context)


@login_required
def process_payment(request):
    """Process a payment via CamPay"""
    try:
        payment_id = request.POST.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        if payment.payment_method == "campay":
            token = get_campay_token()
            response = requests.post(
                f"{CAMPAY_BASE_URL}/collect/",
                headers={"Authorization": f"Token {token}"},
                json={
                    "amount": str(payment.amount),
                    "currency": "XAF",
                    "from": payment.phone_number,
                    "description": f"Payment {payment.id}"
                }
            )

            try:
                data = response.json()
            except Exception:
                data = {"message": "Invalid JSON response from CamPay", "raw": response.text}

            if response.status_code == 200 and data.get("reference"):
                payment.transaction_id = data["reference"]
                payment.status = "processing"
                payment.save()
                return JsonResponse({"status": "processing", "reference": data["reference"]})
            else:
                # Save detailed failure reason
                payment.status = "failed"
                payment.failure_reason = data.get("message", "Unknown error")
                payment.save()

                logger.error(f"CamPay initiation failed: {data}")
                return JsonResponse({
                    "status": "failed",
                    "error": data
                }, status=400)

        return JsonResponse({"error": "Invalid payment method"}, status=400)

    except Exception as e:
        logger.error(f"Payment process error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": "Unable to process payment"
        }, status=500)


def process_campay_payment(payment):
    """Process CamPay payment using the service"""
    try:
        payment.mark_as_processing()
        logger.info(f"Processing CamPay payment {payment.id}")
        
        # Format phone number
        phone_number = payment.phone_number
        if not phone_number.startswith('237'):
            phone_number = campay_service.format_phone_number(phone_number)
        
        logger.info(f"Formatted phone number: {phone_number}")
        
        payment_method = 'campay_mtn'  # Default to MTN
        success, result = campay_service.initiate_payment(
            order=payment.order,
            phone_number=phone_number,
            payment_method=payment_method
        )
        
        if success:
            # Update payment with transaction details
            payment.transaction_id = result.get('transaction_id')
            payment.external_reference = result.get('external_reference', str(payment.order.id))
            payment.provider_response = result
            payment.save()
            
            logger.info(f"CamPay payment initiated: {payment.transaction_id}")
            
            return {
                'success': True,
                'message': result.get('message') or 'Payment request sent. Check your phone.',
                'transaction_id': payment.transaction_id,
                'requires_approval': True
            }
        else:
            error_msg = result.get('error', 'Payment initiation failed')
            logger.error(f"CamPay initiation failed: {error_msg}")
            payment.mark_as_failed(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
            
    except CamPayError as e:
        logger.error(f'CamPay error: {str(e)}')
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': str(e)
        }
    except Exception as e:
        logger.error(f'Payment processing error: {str(e)}', exc_info=True)
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Payment processing failed'
        }


def process_wallet_payment(payment):
    """Process wallet payment"""
    try:
        user = payment.user
        amount = payment.amount
        
        # Check wallet balance
        if not hasattr(user, 'wallet_balance') or user.wallet_balance < amount:
            payment.mark_as_failed('Insufficient wallet balance')
            return {
                'success': False,
                'message': 'Insufficient wallet balance'
            }
        
        # Deduct from wallet
        old_balance = user.wallet_balance
        user.wallet_balance -= amount
        user.save()
        
        # Mark payment as completed
        payment.mark_as_completed()
        
        # Create wallet transaction
        WalletTransaction.objects.create(
            user=user,
            transaction_type='debit',
            source='order_payment',
            amount=amount,
            balance_before=old_balance,
            balance_after=user.wallet_balance,
            payment=payment,
            order=payment.order,
            description=f'Payment for order #{payment.order.order_number}',
            reference=payment.payment_reference
        )
        
        # Update order status
        if payment.order:
            payment.order.status = Order.STATUS_PAID
            payment.order.paid_at = timezone.now()
            payment.order.save()
        
        return {
            'success': True,
            'message': 'Payment completed successfully',
            'transaction_id': payment.payment_reference,
            'requires_approval': False  # Wallet payment is instant
        }
            
    except Exception as e:
        logger.error(f'Wallet payment error: {str(e)}', exc_info=True)
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Payment processing failed'
        }


@login_required
def payment_verification(request, payment_id):
    """Verify payment status"""
    try:
        logger.info(f"Verifying payment status for: {payment_id}")
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)
        
        # Completed or failed
        if payment.status == 'completed':
            logger.info(f"Payment {payment_id} is completed")
            return JsonResponse({
                'status': 'completed',
                'message': 'Payment completed successfully'
            })
        elif payment.status == 'failed':
            logger.info(f"Payment {payment_id} has failed")
            return JsonResponse({
                'status': 'failed',
                'message': payment.failure_reason or 'Payment failed'
            })

        # Pending or processing - check with CamPay
        elif payment.status in ['processing', 'pending']:
            if payment.payment_method == 'campay' and payment.transaction_id:
                logger.info(f"Checking CamPay status for transaction: {payment.transaction_id}")
                result = verify_campay_payment(payment)

                return JsonResponse({
                    'status': result.get('status', 'pending'),
                    'message': result.get('message', 'Awaiting confirmation'),
                    'requires_approval': result.get('requires_approval', True)
                })
        
        # Default response
        return JsonResponse({
            'status': payment.status,
            'message': 'Payment is being processed',
            'requires_approval': True
        })
        
    except Exception as e:
        logger.error(f'Payment verification error: {str(e)}', exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Unable to verify payment status'
        }, status=500)


def verify_campay_payment(payment):
    """Check CamPay payment status"""
    try:
        success, result = campay_service.check_payment_status(payment.transaction_id)
        
        if not success:
            logger.warning(f"Unable to verify payment status for {payment.transaction_id}")
            return {
                'status': 'processing',
                'message': 'Unable to verify payment status'
            }
        
        status = result.get('status', '').upper()
        logger.info(f"CamPay status for {payment.transaction_id}: {status}")
        
        if status == 'SUCCESSFUL':
            # Update payment
            payment.provider_response = result
            payment.save()
            
            # Handle successful payment
            if payment.transaction_type == 'wallet_topup':
                complete_wallet_topup(payment)
            elif payment.order:
                payment.order.status = Order.STATUS_PAID
                payment.order.paid_at = timezone.now()
                payment.order.save()
                logger.info(f"Order {payment.order.order_number} marked as PAID")
            
            payment.mark_as_completed()
            
            return {
                'status': 'completed',
                'message': 'Payment completed successfully'
            }
            
        elif status in ['FAILED', 'CANCELLED']:
            failure_reason = result.get('reason', 'Payment failed')
            payment.mark_as_failed(failure_reason)
            logger.warning(f"Payment {payment.id} failed: {failure_reason}")
            
            return {
                'status': 'failed',
                'message': failure_reason
            }
        else:
            return {
                'status': 'processing',
                'message': 'Payment is being processed'
            }
            
    except Exception as e:
        logger.error(f'CamPay verification error: {str(e)}', exc_info=True)
        return {
            'status': 'processing',
            'message': 'Unable to verify payment status'
        }


@csrf_exempt
@require_http_methods(["POST"])
def campay_webhook(request):
    """Handle CamPay webhook notifications"""
    try:
        payload_raw = request.body.decode('utf-8')
        signature = request.headers.get('X-CamPay-Signature', '')
        
        logger.info("Received CamPay webhook")
        
        # Verify webhook signature
        if not campay_service.verify_webhook(payload_raw, signature):
            logger.warning("Invalid CamPay webhook signature")
            return HttpResponse('Invalid signature', status=400)
        
        # Parse payload
        payload = json.loads(payload_raw)
        logger.info(f"Webhook payload: {payload}")
        
        # Store webhook for audit
        webhook = PaymentWebhook.objects.create(
            provider='campay',
            webhook_data=payload,
            processed=False
        )
        
        # Process the webhook
        transaction_data = campay_service.handle_webhook(payload)
        
        if not transaction_data:
            logger.error("Failed to process CamPay webhook payload")
            return HttpResponse('Invalid payload', status=400)
        
        # Find payment by external_reference (order ID)
        external_ref = transaction_data.get('external_reference')
        if not external_ref:
            logger.error("No external_reference in webhook")
            return HttpResponse('Missing reference', status=400)
        
        try:
            # Find payment by order ID
            payment = Payment.objects.filter(
                order_id=external_ref,
                status__in=['pending', 'processing']
            ).first()
            
            if not payment:
                logger.warning(f'Payment not found for external_reference: {external_ref}')
                return HttpResponse('Payment not found', status=404)
            
            # Update payment with webhook data
            payment.provider_response = payload
            payment.transaction_id = transaction_data.get('reference', payment.transaction_id)
            payment.save()
            
            status = transaction_data.get('status', '').upper()
            logger.info(f"Webhook status for payment {payment.id}: {status}")
            
            if status == 'SUCCESSFUL':
                # Handle successful payment
                if payment.transaction_type == 'wallet_topup':
                    complete_wallet_topup(payment)
                elif payment.order:
                    payment.order.status = Order.STATUS_PAID
                    payment.order.paid_at = timezone.now()
                    payment.order.save()
                    logger.info(f"Order #{payment.order.order_number} marked as paid via webhook")
                
                payment.mark_as_completed()
                
            elif status in ['FAILED', 'CANCELLED']:
                failure_reason = transaction_data.get('reason', 'Payment failed by provider')
                payment.mark_as_failed(failure_reason)
                logger.warning(f"Payment {payment.id} failed via webhook: {failure_reason}")
            
            # Mark webhook as processed
            webhook.payment = payment
            webhook.processed = True
            webhook.processed_at = timezone.now()
            webhook.save()
            
        except Exception as e:
            logger.error(f'Error processing webhook: {str(e)}', exc_info=True)
            return HttpResponse('Processing error', status=500)
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'CamPay webhook error: {str(e)}', exc_info=True)
        return HttpResponse('Error', status=500)


def complete_wallet_topup(payment):
    """Complete wallet top-up after successful payment"""
    try:
        user = payment.user
        amount = payment.amount
        
        # Add to wallet balance
        old_balance = getattr(user, 'wallet_balance', Decimal('0'))
        user.wallet_balance = old_balance + amount
        user.save()
        
        # Create wallet transaction
        WalletTransaction.objects.create(
            user=user,
            transaction_type='credit',
            source='topup',
            amount=amount,
            balance_before=old_balance,
            balance_after=user.wallet_balance,
            payment=payment,
            description=f'Wallet top-up via {payment.get_payment_method_display()}',
            reference=payment.payment_reference
        )
        
        logger.info(f'Wallet top-up completed for user {user.id}: {amount} XAF')
        
    except Exception as e:
        logger.error(f'Wallet top-up completion error: {str(e)}', exc_info=True)
        raise


@login_required
def process_topup(request):
    """Process wallet top-up with CamPay"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        amount = Decimal(data.get('amount', '0'))
        payment_method = data.get('payment_method', 'campay')
        phone_number = data.get('phone_number', '')
        
        # Validate amount
        if amount <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        
        if amount < 100:
            return JsonResponse({'error': 'Minimum top-up amount is 100 XAF'}, status=400)
            
        if amount > 1000000:
            return JsonResponse({'error': 'Maximum top-up amount is 1,000,000 XAF'}, status=400)
        
        # Validate phone number for CamPay
        if payment_method == 'campay' and not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)
        
        with transaction.atomic():
            # Create payment record for top-up
            payment = Payment.objects.create(
                payment_reference=f"TOP_{uuid.uuid4().hex[:12].upper()}",
                user=request.user,
                payment_method=payment_method,
                transaction_type='wallet_topup',
                amount=amount,
                phone_number=phone_number,
                description=f'Wallet top-up for {request.user.get_full_name()}'
            )
            
            # Process payment
            if payment_method == 'campay':
                result = process_campay_topup(payment)
            else:
                return JsonResponse({'error': 'Payment method not supported'}, status=400)
            
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'message': result['message'],
                    'payment_id': str(payment.id),
                    'transaction_id': result.get('transaction_id', ''),
                    'requires_approval': result.get('requires_approval', False)
                })
            else:
                return JsonResponse({'error': result['message']}, status=400)
                
    except Exception as e:
        logger.error(f'Top-up processing error: {str(e)}', exc_info=True)
        return JsonResponse({'error': 'Top-up processing failed'}, status=500)


def process_campay_topup(payment):
    """Process CamPay top-up"""
    try:
        payment.mark_as_processing()
        
        phone_number = campay_service.format_phone_number(payment.phone_number)
        
        # For topup, we don't have an order, so create minimal data
        class TopupOrder:
            def __init__(self, payment):
                self.id = payment.id
                self.total_amount = payment.amount
                self.order_number = payment.payment_reference
        
        topup_order = TopupOrder(payment)
        
        success, result = campay_service.initiate_payment(
            order=topup_order,
            phone_number=phone_number,
            payment_method='campay_mtn'
        )
        
        if success:
            payment.transaction_id = result.get('transaction_id')
            payment.external_reference = result.get('external_reference', str(payment.id))
            payment.provider_response = result
            payment.save()
            
            return {
                'success': True,
                'message': result.get('message'),
                'transaction_id': payment.transaction_id,
                'requires_approval': True
            }
        else:
            payment.mark_as_failed(result.get('error'))
            return {
                'success': False,
                'message': result.get('error', 'Failed to initiate top-up')
            }
            
    except Exception as e:
        logger.error(f'CamPay top-up error: {str(e)}', exc_info=True)
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Top-up processing failed'
        }


@login_required
def payment_success(request, payment_id):
    """Redirect user to the order detail page after successful payment"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if payment.order:
        return redirect('orders:order_detail', order_id=payment.order.id)
    else:
        # If no order is linked (e.g., top-up), redirect to wallet page
        return redirect('wallet:wallet_overview')