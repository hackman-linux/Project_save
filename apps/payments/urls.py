# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment processing
    path('process/', views.process_payment, name='process_payment'),
    path('topup/', views.process_topup, name='process_topup'),
    path('verify/<uuid:payment_id>/', views.payment_verification, name='payment_verification'),
    
    # Payment status and history
    path('status/<str:transaction_id>/', views.payment_status, name='payment_status'),
    path('history/', views.payment_history, name='payment_history'),
    path('wallet/', views.wallet_dashboard, name='wallet_dashboard'),
    
    # CamPay webhook (no auth required)
    path('webhook/campay/', views.campay_webhook, name='campay_webhook'),
    
    # Legacy endpoints (keep for compatibility)
    path('refund/<str:transaction_id>/', views.refund_payment, name='refund_payment'),
]