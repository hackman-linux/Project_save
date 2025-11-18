import csv
import json
import uuid
import logging
from decimal import Decimal
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count, Avg, F
from django.core.paginator import Paginator
from django.conf import settings

from .models import Report, DailySalesReport
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem, MenuCategory
from apps.payments.models import Payment, WalletTransaction
from apps.authentication.models import User

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Reports Management Views
# ----------------------------------------------------------------------

@login_required
def reports_list(request):
    """List all generated reports"""
    if not (request.user.is_canteen_admin() or request.user.is_system_admin()):
        return redirect('dashboard_redirect')

    reports = Report.objects.all().select_related('generated_by').order_by('-created_at')

    # Filter by type
    report_type = request.GET.get('type', 'all')
    if report_type != 'all':
        reports = reports.filter(report_type=report_type)

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        reports = reports.filter(Q(title__icontains=search) | Q(report_type__icontains=search))

    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'report_type': report_type,
        'search': search,
        'report_types': Report.REPORT_TYPES
    }

    return render(request, 'reports/list.html', context)


@login_required
def report_details(request, report_id):
    """View report details"""
    if not (request.user.is_canteen_admin() or request.user.is_system_admin()):
        return redirect('dashboard_redirect')

    report = get_object_or_404(Report, id=report_id)
    return render(request, 'reports/details.html', {'report': report})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_activity_report(request):
    """
    Display a report of user activity.
    """
    return render(request, "system_admin/report.html")



@login_required
def download_report(request, report_id):
    """Download report as CSV"""
    if not (request.user.is_canteen_admin() or request.user.is_system_admin()):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    report = get_object_or_404(Report, id=report_id)

    if report.report_type == 'sales':
        return generate_sales_csv(report.data, report.parameters['start_date'], report.parameters['end_date'])
    elif report.report_type == 'menu_performance':
        return generate_menu_performance_csv(report.data, report.parameters['start_date'], report.parameters['end_date'])
    elif report.report_type == 'user_activity':
        return generate_user_activity_csv(report.data, report.parameters['start_date'], report.parameters['end_date'])
    elif report.report_type == 'financial':
        return generate_financial_csv(report.data, report.parameters['start_date'], report.parameters['end_date'])
    elif report.report_type == 'inventory':
        return generate_inventory_csv(report.data)
    elif report.report_type == 'customer_analytics':
        return generate_customer_analytics_csv(report.data, report.parameters['start_date'], report.parameters['end_date'])
    else:
        return JsonResponse({'error': 'Report type not supported for download'}, status=400)


@login_required
def delete_report(request, report_id):
    """Delete a report"""
    if not request.user.is_system_admin():
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'DELETE':
        try:
            report = get_object_or_404(Report, id=report_id)
            report_title = report.title
            report.delete()
            return JsonResponse({'success': True, 'message': f'Report "{report_title}" deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting report: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ----------------------------------------------------------------------
# CSV Generators
# ----------------------------------------------------------------------

def generate_sales_csv(report_data, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}_to_{end_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Sales Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    writer.writerow(['Order ID', 'Customer', 'Total Amount', 'Status', 'Created At'])
    for order in report_data['orders']:
        writer.writerow([order['id'], order['customer'], order['total'], order['status'], order['created_at']])
    return response


def generate_menu_performance_csv(report_data, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="menu_performance_{start_date}_to_{end_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Menu Performance Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    writer.writerow(['Item Name', 'Category', 'Total Orders', 'Total Quantity', 'Total Revenue (XAF)', 'Average Rating', 'Current Stock'])
    for item in report_data['menu_items']:
        writer.writerow([item['name'], item['category'], item['total_orders'], item['total_quantity'], item['total_revenue'], item['average_rating'], item['current_stock']])
    return response


def generate_user_activity_csv(report_data, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="user_activity_{start_date}_to_{end_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['User Activity Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    writer.writerow(['Name', 'Email', 'Role', 'Orders Count', 'Total Spent (XAF)'])
    for user in report_data['user_orders']:
        writer.writerow([user['name'], user['email'], user['role'], user['orders_count'], user['total_spent']])
    return response


def generate_financial_csv(report_data, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{start_date}_to_{end_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Financial Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    writer.writerow(['Total Revenue (XAF)', report_data['summary']['total_revenue']])
    writer.writerow(['Total Payments', report_data['summary']['total_payments']])
    writer.writerow(['Total Refunds (XAF)', report_data['summary']['total_refunds']])
    writer.writerow(['Net Revenue (XAF)', report_data['summary']['net_revenue']])
    writer.writerow(['Wallet Credits (XAF)', report_data['summary']['wallet_credits']])
    writer.writerow(['Wallet Debits (XAF)', report_data['summary']['wallet_debits']])
    return response


def generate_inventory_csv(report_data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventory_report_{datetime.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Inventory Report'])
    writer.writerow([f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    writer.writerow([])
    writer.writerow(['Item Name', 'Category', 'Current Stock', 'Low Stock Threshold', 'Price (XAF)', 'Inventory Value (XAF)', 'Status', 'Orders (30 days)'])
    for item in report_data['stock_details']:
        writer.writerow([item['name'], item['category'], item['current_stock'], item['low_stock_threshold'], item['price'], item['inventory_value'], item['status'], item['orders_last_30_days']])
    return response


def generate_customer_analytics_csv(report_data, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="customer_analytics_{start_date}_to_{end_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer Analytics Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    writer.writerow(['Name', 'Email', 'Orders Count', 'Total Spent (XAF)', 'Avg Order Value (XAF)', 'Wallet Balance (XAF)'])
    for customer in report_data['top_customers']:
        writer.writerow([customer['name'], customer['email'], customer['orders_count'], customer['total_spent'], customer['avg_order_value'], customer['wallet_balance']])
    return response

# ----------------------------------------------------------------------
# Canteen Admin Reports View (for template rendering)
# ----------------------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def canteen_admin_reports(request):
    """
    Render the Canteen Admin Reports dashboard page.
    """
    if not (request.user.is_canteen_admin() or request.user.is_system_admin()):
        return redirect('dashboard_redirect')

    return render(request, 'canteen_admin/reports.html')


# ----------------------------------------------------------------------
# System Admin Analytics View (for template rendering)
# ----------------------------------------------------------------------


@login_required
def system_admin_reports(request):
    """
    Render the System Admin Analytics dashboard page.
    Includes all required context to prevent VariableDoesNotExist errors.
    """
    if not request.user.is_system_admin():
        return redirect('dashboard_redirect')

    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    # Today's orders
    todays_orders = Order.objects.filter(created_at__date=today)
    completed_orders = todays_orders.filter(status='completed')

    # Yesterday's orders
    yesterday_orders = Order.objects.filter(created_at__date=yesterday)
    yesterday_completed = yesterday_orders.filter(status='completed')

    # Revenue today
    todays_revenue = completed_orders.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    # Revenue yesterday
    yesterday_revenue = yesterday_completed.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    # Completion rate
    if todays_orders.count() > 0:
        completion_rate = (completed_orders.count() / todays_orders.count()) * 100
    else:
        completion_rate = 0

    # Percentage difference vs yesterday
    if yesterday_completed.count() > 0:
        order_change = ((completed_orders.count() - yesterday_completed.count()) /
                        yesterday_completed.count()) * 100
    else:
        order_change = 0

    if yesterday_revenue > 0:
        revenue_change = ((todays_revenue - yesterday_revenue) / yesterday_revenue) * 100
    else:
        revenue_change = 0

    # Top menu items today
    top_items = MenuItem.objects.filter(
        order_items__order__created_at__date=today,
        order_items__order__status='completed'
    ).annotate(
        orders_count=Count('order_items'),
        revenue=Sum('order_items__unit_price' * 1)
    ).order_by('-orders_count')[:5]

    # Global statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(status='active').count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    # Send everything to template
    context = {
        "todays_orders": todays_orders.count(),
        "completed_today": completed_orders.count(),
        "todays_revenue": todays_revenue,
        "completion_rate": round(completion_rate, 1),
        "order_change": round(order_change, 1),
        "revenue_change": round(revenue_change, 1),

        # Global stats
        "total_users": total_users,
        "active_users": active_users,
        "total_orders": total_orders,
        "total_revenue": total_revenue,

        "top_items": top_items,
    }

    return render(request, "system_admin/analytics.html", context)

# ----------------------------------------------------------------------
# Note: All report generators are now standardized and arranged properly.
# ----------------------------------------------------------------------
