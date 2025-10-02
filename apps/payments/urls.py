# apps/payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment pages
    path('payment/<uuid:order_id>/', views.payment_page, name='payment_page'),
    
    # Payment processing
    path('process/', views.process_payment, name='process_payment'),
    path('verify/<uuid:payment_id>/', views.payment_verification, name='payment_verification'),
    
    # Wallet top-up
    path('topup/', views.process_topup, name='process_topup'),
    path("success/<uuid:payment_id>/", views.payment_success, name="payment_success"),
    
    # Webhooks
    path('webhook/campay/', views.campay_webhook, name='campay_webhook'),
]