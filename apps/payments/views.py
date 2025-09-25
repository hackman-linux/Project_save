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
import requests
import logging

import requests
import hashlib
import hmac
import json
import uuid
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
from .models import Payment, WalletTransaction, PaymentProvider, PaymentWebhook
from apps.orders.models import Order
from apps.notifications.models import Notification

logger = logging.getLogger(__name__)

@csrf_exempt
def initiate_payment(request):
    return JsonResponse({"message": "Payment initiation placeholder"})

@login_required
def proceed_to_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, employee=request.user)
    if order.status != "VALIDATED":
        messages.error(request, "Order not validated yet.")
        return redirect("orders:history")
    return render(request, "payment_checkout.html", {"order": order})


@login_required
def payment_status(request, transaction_id):
    return JsonResponse({"transaction_id": transaction_id, "status": "pending"})

@login_required
def refund_payment(request, transaction_id):
    return JsonResponse({"transaction_id": transaction_id, "status": "refunded"})


@login_required
def process_payment(request):
    """Process payment for an order"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_method = data.get('payment_method')
            phone_number = data.get('phone_number', '')
            
            # Get order
            order = get_object_or_404(Order, id=order_id, customer=request.user)
            
            if order.status != 'pending':
                return JsonResponse({'error': 'Order cannot be paid'}, status=400)
            
            # Check if payment already exists
            if order.payments.filter(status__in=['pending', 'completed']).exists():
                return JsonResponse({'error': 'Payment already processed'}, status=400)
            
            with transaction.atomic():
                # Create payment record
                payment = Payment.objects.create(
                    user=request.user,
                    order=order,
                    payment_method=payment_method,
                    amount=order.total_amount,
                    phone_number=phone_number,
                    description=f'Payment for order #{order.order_number}'
                )
                
                # Process payment based on method
                if payment_method == 'wallet':
                    result = process_wallet_payment(payment)
                elif payment_method == 'mtn_momo':
                    result = process_mtn_payment(payment)
                elif payment_method == 'orange_money':
                    result = process_orange_payment(payment)
                else:
                    return JsonResponse({'error': 'Invalid payment method'}, status=400)
                
                if result['success']:
                    # Update order status
                    order.update_status('confirmed', request.user)
                    
                    return JsonResponse({
                        'success': True,
                        'message': result['message'],
                        'payment_id': str(payment.id),
                        'transaction_id': result.get('transaction_id', ''),
                        'redirect_url': result.get('redirect_url', '')
                    })
                else:
                    return JsonResponse({
                        'error': result['message']
                    }, status=400)
                    
        except Exception as e:
            logger.error(f'Payment processing error: {str(e)}')
            return JsonResponse({'error': 'Payment processing failed'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def process_wallet_payment(payment):
    """Process wallet payment"""
    try:
        user = payment.user
        amount = payment.amount
        
        # Check wallet balance
        if not user.has_sufficient_balance(amount):
            payment.mark_as_failed('Insufficient wallet balance')
            return {
                'success': False,
                'message': 'Insufficient wallet balance'
            }
        
        # Deduct from wallet
        old_balance = user.wallet_balance
        if user.deduct_from_wallet(amount):
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
            
            return {
                'success': True,
                'message': 'Payment completed successfully',
                'transaction_id': payment.payment_reference
            }
        else:
            payment.mark_as_failed('Failed to deduct from wallet')
            return {
                'success': False,
                'message': 'Payment failed'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Payment processing failed'
        }


def process_mtn_payment(payment):
    """Process MTN Mobile Money payment"""
    try:
        # Mark payment as processing
        payment.mark_as_processing()
        
        # MTN Mobile Money API integration
        mtn_config = settings.MTN_MOMO_CONFIG
        
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': mtn_config['SUBSCRIPTION_KEY'],
            'Authorization': f'Bearer {get_mtn_access_token()}',
            'X-Reference-Id': str(uuid.uuid4()),
            'X-Target-Environment': 'sandbox'  # Change to 'live' for production
        }
        
        payload = {
            'amount': str(payment.amount),
            'currency': 'XAF',
            'externalId': payment.payment_reference,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': payment.phone_number.replace('+', '')
            },
            'payerMessage': f'Payment for order #{payment.order.order_number}',
            'payeeNote': 'Enterprise Canteen Payment'
        }
        
        response = requests.post(
            f"{mtn_config['BASE_URL']}/collection/v1_0/requesttopay",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 202:
            # Payment request submitted successfully
            transaction_id = headers['X-Reference-Id']
            payment.transaction_id = transaction_id
            payment.save()
            
            return {
                'success': True,
                'message': 'Payment request sent. Please approve on your phone.',
                'transaction_id': transaction_id,
                'requires_approval': True
            }
        else:
            error_message = f'MTN API Error: {response.status_code}'
            payment.mark_as_failed(error_message)
            return {
                'success': False,
                'message': 'Failed to initiate MTN payment'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'MTN payment processing failed'
        }


def process_orange_payment(payment):
    """Process Orange Money payment"""
    try:
        # Mark payment as processing
        payment.mark_as_processing()
        
        # Orange Money API integration
        orange_config = settings.ORANGE_MONEY_CONFIG
        
        # Get access token
        auth_response = requests.post(
            f"{orange_config['BASE_URL']}/oauth/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': orange_config['CLIENT_ID'],
                'client_secret': orange_config['CLIENT_SECRET']
            }
        )
        
        if auth_response.status_code != 200:
            payment.mark_as_failed('Orange authentication failed')
            return {
                'success': False,
                'message': 'Orange Money authentication failed'
            }
        
        access_token = auth_response.json()['access_token']
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        payload = {
            'merchant_key': orange_config['CLIENT_ID'],
            'currency': 'XAF',
            'order_id': payment.payment_reference,
            'amount': int(payment.amount),
            'return_url': orange_config['CALLBACK_URL'],
            'cancel_url': orange_config['CALLBACK_URL'],
            'notif_url': orange_config['CALLBACK_URL'],
            'lang': 'en',
            'reference': f'Order #{payment.order.order_number}'
        }
        
        response = requests.post(
            f"{orange_config['BASE_URL']}/webpayment",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            response_data = response.json()
            payment_url = response_data.get('payment_url')
            transaction_id = response_data.get('pay_token')
            
            payment.transaction_id = transaction_id
            payment.save()
            
            return {
                'success': True,
                'message': 'Redirecting to Orange Money...',
                'transaction_id': transaction_id,
                'redirect_url': payment_url
            }
        else:
            payment.mark_as_failed('Orange API error')
            return {
                'success': False,
                'message': 'Failed to initiate Orange Money payment'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Orange Money processing failed'
        }


def get_mtn_access_token():
    """Get MTN Mobile Money access token"""
    try:
        mtn_config = settings.MTN_MOMO_CONFIG
        
        headers = {
            'Ocp-Apim-Subscription-Key': mtn_config['SUBSCRIPTION_KEY'],
            'Authorization': f'Basic {mtn_config["API_KEY"]}'
        }
        
        response = requests.post(
            f"{mtn_config['BASE_URL']}/collection/token/",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Failed to get MTN access token')
            
    except Exception as e:
        logger.error(f'MTN token error: {str(e)}')
        raise


@login_required
def process_topup(request):
    """Process wallet top-up"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', '0'))
            payment_method = data.get('payment_method')
            phone_number = data.get('phone_number', '')
            
            # Validate amount
            if amount <= 0:
                return JsonResponse({'error': 'Invalid amount'}, status=400)
            
            if amount < 100:  # Minimum top-up amount
                return JsonResponse({'error': 'Minimum top-up amount is 100 XAF'}, status=400)
                
            if amount > 1000000:  # Maximum top-up amount
                return JsonResponse({'error': 'Maximum top-up amount is 1,000,000 XAF'}, status=400)
            
            # Validate payment method
            if payment_method not in ['mtn_momo', 'orange_money']:
                return JsonResponse({'error': 'Invalid payment method for top-up'}, status=400)
            
            # Validate phone number for mobile money
            if not phone_number:
                return JsonResponse({'error': 'Phone number is required'}, status=400)
            
            # Clean phone number format
            phone_number = phone_number.replace(' ', '').replace('-', '')
            if not phone_number.startswith('+'):
                phone_number = '+237' + phone_number
            
            with transaction.atomic():
                # Create payment record for top-up
                payment = Payment.objects.create(
                    user=request.user,
                    payment_method=payment_method,
                    amount=amount,
                    phone_number=phone_number,
                    description=f'Wallet top-up for {request.user.get_full_name()}',
                    payment_type='topup'
                )
                
                # Process payment based on method
                if payment_method == 'mtn_momo':
                    result = process_mtn_topup(payment)
                elif payment_method == 'orange_money':
                    result = process_orange_topup(payment)
                else:
                    return JsonResponse({'error': 'Payment method not supported'}, status=400)
                
                if result['success']:
                    return JsonResponse({
                        'success': True,
                        'message': result['message'],
                        'payment_id': str(payment.id),
                        'transaction_id': result.get('transaction_id', ''),
                        'redirect_url': result.get('redirect_url', ''),
                        'requires_approval': result.get('requires_approval', False)
                    })
                else:
                    return JsonResponse({
                        'error': result['message']
                    }, status=400)
                    
        except Exception as e:
            logger.error(f'Top-up processing error: {str(e)}')
            return JsonResponse({'error': 'Top-up processing failed'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def process_mtn_topup(payment):
    """Process MTN Mobile Money top-up"""
    try:
        # Mark payment as processing
        payment.mark_as_processing()
        
        # MTN Mobile Money API integration
        mtn_config = settings.MTN_MOMO_CONFIG
        
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': mtn_config['SUBSCRIPTION_KEY'],
            'Authorization': f'Bearer {get_mtn_access_token()}',
            'X-Reference-Id': str(uuid.uuid4()),
            'X-Target-Environment': 'sandbox'  # Change to 'live' for production
        }
        
        payload = {
            'amount': str(payment.amount),
            'currency': 'XAF',
            'externalId': payment.payment_reference,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': payment.phone_number.replace('+', '')
            },
            'payerMessage': f'Wallet top-up for {payment.user.get_full_name()}',
            'payeeNote': 'Enterprise Canteen Wallet Top-up'
        }
        
        response = requests.post(
            f"{mtn_config['BASE_URL']}/collection/v1_0/requesttopay",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 202:
            # Payment request submitted successfully
            transaction_id = headers['X-Reference-Id']
            payment.transaction_id = transaction_id
            payment.save()
            
            return {
                'success': True,
                'message': 'Top-up request sent. Please approve on your phone.',
                'transaction_id': transaction_id,
                'requires_approval': True
            }
        else:
            error_message = f'MTN API Error: {response.status_code}'
            payment.mark_as_failed(error_message)
            return {
                'success': False,
                'message': 'Failed to initiate MTN top-up'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'MTN top-up processing failed'
        }


def process_orange_topup(payment):
    """Process Orange Money top-up"""
    try:
        # Mark payment as processing
        payment.mark_as_processing()
        
        # Orange Money API integration
        orange_config = settings.ORANGE_MONEY_CONFIG
        
        # Get access token
        auth_response = requests.post(
            f"{orange_config['BASE_URL']}/oauth/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': orange_config['CLIENT_ID'],
                'client_secret': orange_config['CLIENT_SECRET']
            }
        )
        
        if auth_response.status_code != 200:
            payment.mark_as_failed('Orange authentication failed')
            return {
                'success': False,
                'message': 'Orange Money authentication failed'
            }
        
        access_token = auth_response.json()['access_token']
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        payload = {
            'merchant_key': orange_config['CLIENT_ID'],
            'currency': 'XAF',
            'order_id': payment.payment_reference,
            'amount': int(payment.amount),
            'return_url': orange_config['CALLBACK_URL'],
            'cancel_url': orange_config['CALLBACK_URL'],
            'notif_url': orange_config['CALLBACK_URL'],
            'lang': 'en',
            'reference': f'Wallet top-up for {payment.user.get_full_name()}'
        }
        
        response = requests.post(
            f"{orange_config['BASE_URL']}/webpayment",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            response_data = response.json()
            payment_url = response_data.get('payment_url')
            transaction_id = response_data.get('pay_token')
            
            payment.transaction_id = transaction_id
            payment.save()
            
            return {
                'success': True,
                'message': 'Redirecting to Orange Money...',
                'transaction_id': transaction_id,
                'redirect_url': payment_url
            }
        else:
            payment.mark_as_failed('Orange API error')
            return {
                'success': False,
                'message': 'Failed to initiate Orange Money top-up'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Orange Money top-up processing failed'
        }


@login_required
def process_topup(request):
    """
    Allow employee to top up their wallet balance.
    For now we simulate the topup (e.g., via cash or external payment).
    """

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")

            # Create wallet transaction
            WalletTransaction.objects.create(
                employee=request.user,
                amount=amount,
                transaction_type="credit",
                description="Wallet Top-up",
                created_at=timezone.now(),
            )

            messages.success(request, f"Wallet successfully topped up with {amount} XAF.")
            return redirect("employee_dashboard")

        except Exception as e:
            messages.error(request, f"Invalid amount: {e}")

    return render(request, "employee/process_topup.html")


@login_required
def payment_history(request):
    """Display user payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by payment type
    payment_type = request.GET.get('type', 'all')
    if payment_type != 'all':
        payments = payments.filter(payment_type=payment_type)
    
    # Filter by status
    status = request.GET.get('status', 'all')
    if status != 'all':
        payments = payments.filter(status=status)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'payment_type': payment_type,
        'status': status,
    }
    
    return render(request, 'payments/history.html', context)


@login_required
def payment_verification(request, payment_id):
    """Verify payment status"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.status == 'completed':
        return JsonResponse({
            'status': 'completed',
            'message': 'Payment completed successfully'
        })
    elif payment.status == 'failed':
        return JsonResponse({
            'status': 'failed',
            'message': 'Payment failed'
        })
    elif payment.status == 'processing':
        # Check payment status with provider
        if payment.payment_method == 'mtn_momo':
            result = verify_mtn_payment(payment)
        elif payment.payment_method == 'orange_money':
            result = verify_orange_payment(payment)
        else:
            result = {'status': 'processing'}
        
        return JsonResponse(result)
    else:
        return JsonResponse({
            'status': 'pending',
            'message': 'Payment is pending'
        })


def verify_mtn_payment(payment):
    """Verify MTN Mobile Money payment status"""
    try:
        mtn_config = settings.MTN_MOMO_CONFIG
        
        headers = {
            'Ocp-Apim-Subscription-Key': mtn_config['SUBSCRIPTION_KEY'],
            'Authorization': f'Bearer {get_mtn_access_token()}',
            'X-Target-Environment': 'sandbox'
        }
        
        response = requests.get(
            f"{mtn_config['BASE_URL']}/collection/v1_0/requesttopay/{payment.transaction_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', '').upper()
            
            if status == 'SUCCESSFUL':
                # Process successful payment
                if payment.payment_type == 'topup':
                    complete_wallet_topup(payment)
                payment.mark_as_completed()
                
                return {'status': 'completed', 'message': 'Payment completed successfully'}
            elif status == 'FAILED':
                payment.mark_as_failed('Payment failed by provider')
                return {'status': 'failed', 'message': 'Payment failed'}
            else:
                return {'status': 'processing', 'message': 'Payment is being processed'}
        else:
            return {'status': 'processing', 'message': 'Unable to verify payment status'}
            
    except Exception as e:
        logger.error(f'MTN verification error: {str(e)}')
        return {'status': 'processing', 'message': 'Unable to verify payment status'}


def verify_orange_payment(payment):
    """Verify Orange Money payment status"""
    try:
        orange_config = settings.ORANGE_MONEY_CONFIG
        
        # Get access token
        auth_response = requests.post(
            f"{orange_config['BASE_URL']}/oauth/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': orange_config['CLIENT_ID'],
                'client_secret': orange_config['CLIENT_SECRET']
            }
        )
        
        if auth_response.status_code != 200:
            return {'status': 'processing', 'message': 'Unable to verify payment status'}
        
        access_token = auth_response.json()['access_token']
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(
            f"{orange_config['BASE_URL']}/webpayment/{payment.transaction_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', '').upper()
            
            if status == 'SUCCESS':
                # Process successful payment
                if payment.payment_type == 'topup':
                    complete_wallet_topup(payment)
                payment.mark_as_completed()
                
                return {'status': 'completed', 'message': 'Payment completed successfully'}
            elif status in ['FAILED', 'EXPIRED']:
                payment.mark_as_failed('Payment failed by provider')
                return {'status': 'failed', 'message': 'Payment failed'}
            else:
                return {'status': 'processing', 'message': 'Payment is being processed'}
        else:
            return {'status': 'processing', 'message': 'Unable to verify payment status'}
            
    except Exception as e:
        logger.error(f'Orange verification error: {str(e)}')
        return {'status': 'processing', 'message': 'Unable to verify payment status'}


def complete_wallet_topup(payment):
    """Complete wallet top-up after successful payment"""
    try:
        user = payment.user
        amount = payment.amount
        
        # Add to wallet balance
        old_balance = user.wallet_balance
        user.add_to_wallet(amount)
        
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
        
        # Create notification
        Notification.objects.create(
            user=user,
            title='Wallet Top-up Successful',
            message=f'Your wallet has been topped up with {amount} XAF. New balance: {user.wallet_balance} XAF',
            notification_type='payment'
        )
        
        logger.info(f'Wallet top-up completed for user {user.id}: {amount} XAF')
        
    except Exception as e:
        logger.error(f'Wallet top-up completion error: {str(e)}')
        raise


@csrf_exempt
@require_http_methods(["POST"])
def mtn_webhook(request):
    """Handle MTN Mobile Money webhooks"""
    try:
        data = json.loads(request.body)
        
        # Store webhook data
        PaymentWebhook.objects.create(
            provider='mtn',
            event_type=data.get('event_type', 'unknown'),
            data=data
        )
        
        # Process webhook
        reference_id = data.get('reference_id')
        status = data.get('status', '').upper()
        
        if reference_id:
            try:
                payment = Payment.objects.get(transaction_id=reference_id)
                
                if status == 'SUCCESSFUL':
                    if payment.payment_type == 'topup':
                        complete_wallet_topup(payment)
                    payment.mark_as_completed()
                elif status == 'FAILED':
                    payment.mark_as_failed('Payment failed by provider')
                    
            except Payment.DoesNotExist:
                logger.warning(f'Payment not found for MTN webhook: {reference_id}')
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'MTN webhook error: {str(e)}')
        return HttpResponse('Error', status=500)


@csrf_exempt
@require_http_methods(["POST"])
def orange_webhook(request):
    """Handle Orange Money webhooks"""
    try:
        data = json.loads(request.body)
        
        # Store webhook data
        PaymentWebhook.objects.create(
            provider='orange',
            event_type=data.get('event_type', 'unknown'),
            data=data
        )
        
        # Process webhook
        order_id = data.get('order_id')
        status = data.get('status', '').upper()
        
        if order_id:
            try:
                payment = Payment.objects.get(transaction_id=order_id)
                
                if status == 'SUCCESS':
                    if payment.payment_type == 'topup':
                        complete_wallet_topup(payment)
                    payment.mark_as_completed()
                elif status in ['FAILED', 'EXPIRED']:
                    payment.mark_as_failed('Payment failed by provider')
                    
            except Payment.DoesNotExist:
                logger.warning(f'Payment not found for Orange webhook: {order_id}')
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'Orange webhook error: {str(e)}')
        return HttpResponse('Error', status=500)


@login_required
def wallet_dashboard(request):
    """Wallet dashboard for users"""
    user = request.user
    
    # Get recent transactions
    recent_transactions = WalletTransaction.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    # Get wallet statistics
    total_credited = WalletTransaction.objects.filter(
        user=user,
        transaction_type='credit'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    total_debited = WalletTransaction.objects.filter(
        user=user,
        transaction_type='debit'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    context = {
        'wallet_balance': user.wallet_balance,
        'recent_transactions': recent_transactions,
        'total_credited': total_credited,
        'total_debited': total_debited,
    }
    
    return render(request, 'payments/wallet_dashboard.html', context)

# Add this to your existing payments/views.py

import requests
from django.conf import settings
import hashlib
import hmac
from decimal import Decimal

# CamPay Payment Integration
def process_campay_payment(payment):
    """Process CamPay Mobile Money payment"""
    try:
        # Mark payment as processing
        payment.mark_as_processing()
        
        # CamPay configuration
        campay_config = settings.CAMPAY_CONFIG
        
        # Generate signature for security
        data_to_sign = f"{payment.payment_reference}{payment.amount}{campay_config['SECRET_KEY']}"
        signature = hmac.new(
            campay_config['SECRET_KEY'].encode('utf-8'),
            data_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': campay_config['API_KEY'],
            'Authorization': f'Bearer {get_campay_access_token()}'
        }
        
        payload = {
            'amount': str(payment.amount),
            'currency': 'XAF',
            'from': payment.phone_number.replace('+', '').replace(' ', ''),
            'description': payment.description or f'Payment for order #{payment.order.order_number if payment.order else "wallet top-up"}',
            'external_reference': payment.payment_reference,
            'redirect_url': f"{settings.BASE_URL}/payments/callback/campay/",
            'webhook_url': f"{settings.BASE_URL}/payments/webhook/campay/",
            'signature': signature
        }
        
        response = requests.post(
            f"{campay_config['BASE_URL']}/api/collect/",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'SUCCESS':
                transaction_id = response_data.get('reference')
                payment.transaction_id = transaction_id
                payment.external_reference = response_data.get('external_reference', '')
                payment.provider_response = response_data
                payment.save()
                
                return {
                    'success': True,
                    'message': 'Payment request sent. Please approve on your phone.',
                    'transaction_id': transaction_id,
                    'requires_approval': True,
                    'ussd_code': response_data.get('ussd_code', '')
                }
            else:
                error_message = response_data.get('message', 'Payment initiation failed')
                payment.mark_as_failed(error_message)
                return {
                    'success': False,
                    'message': error_message
                }
        else:
            error_message = f'CamPay API Error: {response.status_code} - {response.text}'
            payment.mark_as_failed(error_message)
            return {
                'success': False,
                'message': 'Failed to initiate CamPay payment'
            }
            
    except Exception as e:
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'CamPay payment processing failed'
        }


def get_campay_access_token():
    """Get CamPay access token"""
    try:
        campay_config = settings.CAMPAY_CONFIG
        
        payload = {
            'username': campay_config['USERNAME'],
            'password': campay_config['PASSWORD']
        }
        
        response = requests.post(
            f"{campay_config['BASE_URL']}/api/token/",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get('token')
        else:
            raise Exception('Failed to get CamPay access token')
            
    except Exception as e:
        logger.error(f'CamPay token error: {str(e)}')
        raise


def verify_campay_payment(payment):
    """Verify CamPay payment status"""
    try:
        campay_config = settings.CAMPAY_CONFIG
        
        headers = {
            'X-API-KEY': campay_config['API_KEY'],
            'Authorization': f'Bearer {get_campay_access_token()}'
        }
        
        response = requests.get(
            f"{campay_config['BASE_URL']}/api/transaction/{payment.transaction_id}/",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', '').upper()
            
            if status in ['SUCCESSFUL', 'COMPLETED']:
                # Update payment with provider response
                payment.provider_response = data
                payment.save()
                
                # Process successful payment
                if payment.transaction_type == 'wallet_topup':
                    complete_wallet_topup(payment)
                elif payment.order:
                    # Update order status to paid
                    payment.order.status = payment.order.STATUS_PAID
                    payment.order.paid_at = timezone.now()
                    payment.order.payment_method = payment.payment_method
                    payment.order.save()
                
                payment.mark_as_completed(payment.transaction_id)
                
                # Send success notification
                send_payment_success_notification(payment)
                
                return {'status': 'completed', 'message': 'Payment completed successfully'}
                
            elif status in ['FAILED', 'CANCELLED']:
                failure_reason = data.get('reason', 'Payment failed by provider')
                payment.mark_as_failed(failure_reason)
                
                # Send failure notification
                send_payment_failure_notification(payment, failure_reason)
                
                return {'status': 'failed', 'message': failure_reason}
            else:
                return {'status': 'processing', 'message': 'Payment is being processed'}
        else:
            return {'status': 'processing', 'message': 'Unable to verify payment status'}
            
    except Exception as e:
        logger.error(f'CamPay verification error: {str(e)}')
        return {'status': 'processing', 'message': 'Unable to verify payment status'}


@csrf_exempt
@require_http_methods(["POST"])
def campay_webhook(request):
    """Handle CamPay webhooks"""
    try:
        data = json.loads(request.body)
        
        # Verify webhook signature for security
        signature = request.headers.get('X-CamPay-Signature', '')
        expected_signature = hmac.new(
            settings.CAMPAY_CONFIG['SECRET_KEY'].encode('utf-8'),
            request.body,
            hashlib.sha256
        ).hexdigest()
        
        if signature != expected_signature:
            logger.warning('Invalid CamPay webhook signature')
            return HttpResponse('Invalid signature', status=400)
        
        # Store webhook data
        PaymentWebhook.objects.create(
            provider='campay',
            webhook_data=data
        )
        
        # Process webhook
        external_reference = data.get('external_reference')
        status = data.get('status', '').upper()
        
        if external_reference:
            try:
                payment = Payment.objects.get(payment_reference=external_reference)
                payment.provider_response = data
                payment.save()
                
                if status in ['SUCCESSFUL', 'COMPLETED']:
                    if payment.transaction_type == 'wallet_topup':
                        complete_wallet_topup(payment)
                    elif payment.order:
                        # Update order status
                        payment.order.status = payment.order.STATUS_PAID
                        payment.order.paid_at = timezone.now()
                        payment.order.payment_method = payment.payment_method
                        payment.order.save()
                        
                        # Send order paid notification
                        send_order_paid_notification(payment.order)
                    
                    payment.mark_as_completed(data.get('reference'))
                    send_payment_success_notification(payment)
                    
                elif status in ['FAILED', 'CANCELLED']:
                    failure_reason = data.get('reason', 'Payment failed by provider')
                    payment.mark_as_failed(failure_reason)
                    send_payment_failure_notification(payment, failure_reason)
                    
            except Payment.DoesNotExist:
                logger.warning(f'Payment not found for CamPay webhook: {external_reference}')
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'CamPay webhook error: {str(e)}')
        return HttpResponse('Error', status=500)


# Update your process_payment function to include CamPay
def process_payment_updated(request):
    """Updated process payment function with CamPay integration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_method = data.get('payment_method')
            phone_number = data.get('phone_number', '')
            
            # Get order
            order = get_object_or_404(Order, id=order_id, employee=request.user)
            
            if order.status != Order.STATUS_VALIDATED:
                return JsonResponse({'error': 'Order is not validated yet'}, status=400)
            
            # Check if payment already exists
            if order.payments.filter(status__in=['pending', 'processing', 'completed']).exists():
                return JsonResponse({'error': 'Payment already processed'}, status=400)
            
            with transaction.atomic():
                # Generate unique payment reference
                payment_reference = f"PAY_{uuid.uuid4().hex[:12].upper()}"
                
                # Create payment record
                payment = Payment.objects.create(
                    payment_reference=payment_reference,
                    user=request.user,
                    order=order,
                    payment_method=payment_method,
                    transaction_type='order_payment',
                    amount=order.total_amount,
                    phone_number=phone_number,
                    description=f'Payment for order #{order.order_number}'
                )
                
                # Process payment based on method
                if payment_method == 'wallet':
                    result = process_wallet_payment(payment)
                elif payment_method == 'campay':
                    result = process_campay_payment(payment)
                elif payment_method == 'mtn_momo':
                    result = process_mtn_payment(payment)
                elif payment_method == 'orange_money':
                    result = process_orange_payment(payment)
                else:
                    return JsonResponse({'error': 'Invalid payment method'}, status=400)
                
                if result['success']:
                    return JsonResponse({
                        'success': True,
                        'message': result['message'],
                        'payment_id': str(payment.id),
                        'transaction_id': result.get('transaction_id', ''),
                        'redirect_url': result.get('redirect_url', ''),
                        'requires_approval': result.get('requires_approval', False),
                        'ussd_code': result.get('ussd_code', '')
                    })
                else:
                    return JsonResponse({
                        'error': result['message']
                    }, status=400)
                    
        except Exception as e:
            logger.error(f'Payment processing error: {str(e)}')
            return JsonResponse({'error': 'Payment processing failed'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Notification functions
def send_payment_success_notification(payment):
    """Send payment success notification"""
    try:
        from apps.notifications.models import Notification
        
        if payment.transaction_type == 'wallet_topup':
            title = 'Wallet Top-up Successful'
            message = f'Your wallet has been topped up with {payment.amount} XAF successfully.'
        else:
            title = 'Payment Successful'
            message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} completed successfully.'
        
        Notification.objects.create(
            target_user=payment.user,
            title=title,
            message=message,
            notification_type='payment_success',
            priority='normal',
            order=payment.order,
            action_url=f'/orders/{payment.order.id}/detail/' if payment.order else '/payments/history/',
            action_text='View Details',
            created_by=None
        )
        
        # Send email notification
        send_payment_email_notification(payment, 'success')
        
    except Exception as e:
        logger.error(f'Error sending payment success notification: {str(e)}')


def send_payment_failure_notification(payment, reason):
    """Send payment failure notification"""
    try:
        from apps.notifications.models import Notification
        
        if payment.transaction_type == 'wallet_topup':
            title = 'Wallet Top-up Failed'
            message = f'Your wallet top-up of {payment.amount} XAF failed. Reason: {reason}'
        else:
            title = 'Payment Failed'
            message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} failed. Reason: {reason}'
        
        Notification.objects.create(
            target_user=payment.user,
            title=title,
            message=message,
            notification_type='payment_failed',
            priority='high',
            order=payment.order,
            action_url=f'/orders/{payment.order.id}/payment/' if payment.order else '/payments/topup/',
            action_text='Try Again',
            created_by=None
        )
        
        # Send email notification
        send_payment_email_notification(payment, 'failure', reason)
        
    except Exception as e:
        logger.error(f'Error sending payment failure notification: {str(e)}')


def send_order_paid_notification(order):
    """Send notification when order is paid"""
    try:
        from apps.notifications.models import Notification
        
        # Notify customer
        Notification.objects.create(
            target_user=order.employee,
            title=f'Order #{order.order_number} Payment Confirmed',
            message=f'Payment for your order #{order.order_number} has been confirmed. Your order is now being prepared.',
            notification_type='order_status',
            priority='normal',
            order=order,
            action_url=f'/orders/{order.id}/detail/',
            action_text='View Order',
            created_by=None
        )
        
        # Notify canteen admins
        Notification.objects.create(
            target_audience='canteen_admins',
            title=f'Order #{order.order_number} Paid',
            message=f'Order #{order.order_number} by {order.employee.get_full_name() or order.employee.username} has been paid and is ready for preparation.',
            notification_type='order_status',
            priority='normal',
            order=order,
            action_url=f'/admin/orders/{order.id}/details/',
            action_text='View Order',
            created_by=None
        )
        
    except Exception as e:
        logger.error(f'Error sending order paid notification: {str(e)}')


def send_payment_email_notification(payment, status, reason=None):
    """Send payment email notification"""
    try:
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        
        if not hasattr(settings, 'EMAIL_HOST') or not settings.DEFAULT_FROM_EMAIL:
            return
        
        if status == 'success':
            subject = f'Payment Confirmation - {payment.amount} XAF'
            if payment.transaction_type == 'wallet_topup':
                template = 'payments/emails/topup_success.html'
            else:
                template = 'payments/emails/payment_success.html'
        else:
            subject = f'Payment Failed - {payment.amount} XAF'
            if payment.transaction_type == 'wallet_topup':
                template = 'payments/emails/topup_failed.html'
            else:
                template = 'payments/emails/payment_failed.html'
        
        context = {
            'user': payment.user,
            'payment': payment,
            'order': payment.order,
            'reason': reason
        }
        
        html_message = render_to_string(template, context)
        
        send_mail(
            subject=subject,
            message='',  # Plain text version can be added
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payment.user.email],
            html_message=html_message,
            fail_silently=True
        )
        
    except Exception as e:
        logger.error(f'Error sending payment email: {str(e)}')

# Add these functions to your payments/views.py


def process_campay_payment(payment):
    """Process CamPay payment (handles MTN, Orange, etc. automatically)"""
    try:
        payment.mark_as_processing()
        
        campay_config = settings.CAMPAY_CONFIG
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': campay_config['API_KEY']
        }
        
        # CamPay collect request payload
        payload = {
            'amount': int(payment.amount),  # CamPay expects integer amount
            'currency': 'XAF',
            'from': payment.phone_number.replace('+', '').replace(' ', ''),
            'description': payment.description or f'Order #{payment.order.order_number}',
            'external_reference': payment.payment_reference,
        }
        
        response = requests.post(
            f"{campay_config['BASE_URL']}/collect/",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data.get('status') == 'PENDING':
                # Payment initiated successfully
                payment.transaction_id = response_data.get('reference')
                payment.external_reference = response_data.get('external_reference')
                payment.provider_response = response_data
                payment.save()
                
                return {
                    'success': True,
                    'message': 'Payment request sent. Please check your phone for approval.',
                    'transaction_id': payment.transaction_id,
                    'requires_approval': True,
                    'ussd_code': response_data.get('ussd_code', '')
                }
            else:
                error_message = response_data.get('message', 'Payment initiation failed')
                payment.mark_as_failed(error_message)
                return {
                    'success': False,
                    'message': error_message
                }
        else:
            error_message = f'CamPay API Error: {response.status_code}'
            try:
                error_data = response.json()
                error_message += f" - {error_data.get('message', response.text)}"
            except:
                error_message += f" - {response.text}"
            
            payment.mark_as_failed(error_message)
            return {
                'success': False,
                'message': 'Failed to initiate payment. Please try again.'
            }
            
    except Exception as e:
        logger.error(f'CamPay payment error: {str(e)}')
        payment.mark_as_failed(str(e))
        return {
            'success': False,
            'message': 'Payment processing failed. Please try again.'
        }


def verify_campay_payment(payment):
    """Check CamPay payment status"""
    try:
        campay_config = settings.CAMPAY_CONFIG
        
        headers = {
            'X-API-KEY': campay_config['API_KEY']
        }
        
        response = requests.get(
            f"{campay_config['BASE_URL']}/transaction/{payment.transaction_id}/",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', '').upper()
            
            if status == 'SUCCESSFUL':
                # Payment completed successfully
                payment.provider_response = data
                payment.save()
                
                # Handle successful payment
                if payment.transaction_type == 'wallet_topup':
                    complete_wallet_topup(payment)
                elif payment.order:
                    # Update order status
                    payment.order.status = payment.order.STATUS_PAID
                    payment.order.paid_at = timezone.now()
                    payment.order.payment_method = payment.payment_method
                    payment.order.save()
                    
                    # Send order paid notification
                    send_order_paid_notification(payment.order)
                
                payment.mark_as_completed()
                send_payment_success_notification(payment)
                
                return {'status': 'completed', 'message': 'Payment completed successfully'}
                
            elif status in ['FAILED', 'CANCELLED']:
                failure_reason = data.get('reason', 'Payment failed')
                payment.mark_as_failed(failure_reason)
                send_payment_failure_notification(payment, failure_reason)
                
                return {'status': 'failed', 'message': failure_reason}
            else:
                return {'status': 'processing', 'message': 'Payment is being processed'}
        else:
            return {'status': 'processing', 'message': 'Unable to verify payment status'}
            
    except Exception as e:
        logger.error(f'CamPay verification error: {str(e)}')
        return {'status': 'processing', 'message': 'Unable to verify payment status'}


@csrf_exempt
@require_http_methods(["POST"])
def campay_webhook(request):
    """Handle CamPay webhook notifications"""
    try:
        data = json.loads(request.body)
        
        # Store webhook for audit
        from .models import PaymentWebhook
        PaymentWebhook.objects.create(
            provider='campay',
            webhook_data=data,
            processed=False
        )
        
        # Process the webhook
        external_reference = data.get('external_reference')
        status = data.get('status', '').upper()
        
        if external_reference:
            try:
                from .models import Payment
                payment = Payment.objects.get(payment_reference=external_reference)
                
                # Update payment with response data
                payment.provider_response = data
                payment.save()
                
                if status == 'SUCCESSFUL':
                    # Handle successful payment
                    if payment.transaction_type == 'wallet_topup':
                        complete_wallet_topup(payment)
                    elif payment.order:
                        # Update order status
                        payment.order.status = payment.order.STATUS_PAID
                        payment.order.paid_at = timezone.now()
                        payment.order.payment_method = payment.payment_method
                        payment.order.save()
                        
                        # Send notifications
                        send_order_paid_notification(payment.order)
                    
                    payment.mark_as_completed(data.get('reference'))
                    send_payment_success_notification(payment)
                    
                elif status in ['FAILED', 'CANCELLED']:
                    failure_reason = data.get('reason', 'Payment failed by provider')
                    payment.mark_as_failed(failure_reason)
                    send_payment_failure_notification(payment, failure_reason)
                
                # Mark webhook as processed
                webhook = PaymentWebhook.objects.filter(
                    provider='campay',
                    webhook_data=data
                ).first()
                if webhook:
                    webhook.processed = True
                    webhook.processed_at = timezone.now()
                    webhook.save()
                    
            except Payment.DoesNotExist:
                logger.warning(f'Payment not found for CamPay webhook: {external_reference}')
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'CamPay webhook error: {str(e)}')
        return HttpResponse('Error', status=500)


# Enhanced process_payment function with CamPay
@login_required
def process_payment(request):
    """Process payment with CamPay integration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_method = data.get('payment_method')
            phone_number = data.get('phone_number', '')
            
            # Get and validate order
            from apps.orders.models import Order
            order = get_object_or_404(Order, id=order_id, employee=request.user)
            
            if order.status != Order.STATUS_VALIDATED:
                return JsonResponse({'error': 'Order is not validated yet'}, status=400)
            
            # Check if payment already exists
            if order.payments.filter(status__in=['pending', 'processing', 'completed']).exists():
                return JsonResponse({'error': 'Payment already processed'}, status=400)
            
            # Validate phone number for mobile money
            if payment_method == 'campay' and not phone_number:
                return JsonResponse({'error': 'Phone number is required for mobile money payment'}, status=400)
            
            with transaction.atomic():
                # Create payment record
                from .models import Payment
                payment = Payment.objects.create(
                    payment_reference=f"PAY_{uuid.uuid4().hex[:12].upper()}",
                    user=request.user,
                    order=order,
                    payment_method=payment_method,
                    transaction_type='order_payment',
                    amount=order.total_amount,
                    phone_number=phone_number,
                    description=f'Payment for order #{order.order_number}'
                )
                
                # Process payment based on method
                if payment_method == 'wallet':
                    result = process_wallet_payment(payment)
                elif payment_method == 'campay':
                    result = process_campay_payment(payment)
                else:
                    return JsonResponse({'error': 'Invalid payment method'}, status=400)
                
                if result['success']:
                    return JsonResponse({
                        'success': True,
                        'message': result['message'],
                        'payment_id': str(payment.id),
                        'transaction_id': result.get('transaction_id', ''),
                        'requires_approval': result.get('requires_approval', False),
                        'ussd_code': result.get('ussd_code', '')
                    })
                else:
                    return JsonResponse({'error': result['message']}, status=400)
                    
        except Exception as e:
            logger.error(f'Payment processing error: {str(e)}')
            return JsonResponse({'error': 'Payment processing failed'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Enhanced topup processing with CamPay
@login_required
def process_topup(request):
    """Process wallet top-up with CamPay"""
    if request.method == 'POST':
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
                from .models import Payment
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
                    result = process_campay_payment(payment)
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
            logger.error(f'Top-up processing error: {str(e)}')
            return JsonResponse({'error': 'Top-up processing failed'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Notification helper functions (already defined in previous artifact)
def send_payment_success_notification(payment):
    """Send payment success notification"""
    try:
        from apps.notifications.models import Notification
        
        if payment.transaction_type == 'wallet_topup':
            title = 'Wallet Top-up Successful'
            message = f'Your wallet has been topped up with {payment.amount} XAF successfully.'
            action_url = '/payments/history/'
            action_text = 'View History'
        else:
            title = 'Payment Successful'
            message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} completed successfully.'
            action_url = f'/orders/{payment.order.id}/detail/'
            action_text = 'View Order'
        
        Notification.objects.create(
            target_user=payment.user,
            title=title,
            message=message,
            notification_type='payment_success',
            priority='normal',
            order=payment.order,
            action_url=action_url,
            action_text=action_text,
            created_by=None
        )
        
    except Exception as e:
        logger.error(f'Error sending payment success notification: {str(e)}')


def send_payment_failure_notification(payment, reason):
    """Send payment failure notification"""
    try:
        from apps.notifications.models import Notification
        
        if payment.transaction_type == 'wallet_topup':
            title = 'Wallet Top-up Failed'
            message = f'Your wallet top-up of {payment.amount} XAF failed. Reason: {reason}'
            action_url = '/payments/topup/'
            action_text = 'Try Again'
        else:
            title = 'Payment Failed'
            message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} failed. Reason: {reason}'
            action_url = f'/orders/{payment.order.id}/payment/'
            action_text = 'Try Again'
        
        Notification.objects.create(
            target_user=payment.user,
            title=title,
            message=message,
            notification_type='payment_failed',
            priority='high',
            order=payment.order,
            action_url=action_url,
            action_text=action_text,
            created_by=None
        )
        
    except Exception as e:
        logger.error(f'Error sending payment failure notification: {str(e)}')


def send_order_paid_notification(order):
    """Send notification when order is paid"""
    try:
        from apps.notifications.models import Notification
        
        # Notify customer
        Notification.objects.create(
            target_user=order.employee,
            title=f'Order #{order.order_number} Payment Confirmed',
            message=f'Payment confirmed! Your order is now being prepared by our kitchen team.',
            notification_type='order_status',
            priority='normal',
            order=order,
            action_url=f'/orders/{order.id}/detail/',
            action_text='Track Order',
            created_by=None
        )
        
        # Notify canteen admins
        Notification.objects.create(
            target_audience='canteen_admins',
            title=f'Order #{order.order_number} Paid',
            message=f'Order #{order.order_number} by {order.employee.get_full_name() or order.employee.username} has been paid and is ready for preparation.',
            notification_type='order_status',
            priority='normal',
            order=order,
            action_url=f'/admin/orders/{order.id}/details/',
            action_text='View Order',
            created_by=None
        )
        
    except Exception as e:
        logger.error(f'Error sending order paid notification: {str(e)}')