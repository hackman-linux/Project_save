# Save as: apps/payments/management/commands/test_campay.py

from django.core.management.base import BaseCommand
from apps.payments.services.campay_services import campay_service, CamPayError
import sys

class Command(BaseCommand):
    help = 'Test CamPay API connection and authentication'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('Testing CamPay Integration'))
        self.stdout.write(self.style.WARNING('=' * 70))
        
        # Test 1: Configuration
        self.stdout.write('\n1. Checking Configuration...')
        config = campay_service.config
        
        self.stdout.write(f"   Base URL: {config.get('BASE_URL')}")
        self.stdout.write(f"   Environment: {config.get('ENVIRONMENT')}")
        self.stdout.write(f"   Username set: {'Yes' if config.get('USERNAME') else 'No'}")
        self.stdout.write(f"   Password set: {'Yes' if config.get('PASSWORD') else 'No'}")
        self.stdout.write(f"   API Key set: {'Yes' if config.get('API_KEY') else 'No'}")
        
        if not config.get('USERNAME') and not config.get('API_KEY'):
            self.stdout.write(self.style.ERROR('\n   ERROR: No credentials configured!'))
            self.stdout.write(self.style.WARNING('   Please set CAMPAY_USERNAME and CAMPAY_PASSWORD'))
            self.stdout.write(self.style.WARNING('   or CAMPAY_API_KEY in your .env file'))
            sys.exit(1)
        
        # Test 2: Authentication
        self.stdout.write('\n2. Testing Authentication...')
        try:
            if config.get('USERNAME'):
                token = campay_service._get_auth_token()
                self.stdout.write(self.style.SUCCESS(f'   ✓ Token obtained: {token[:30]}...'))
            else:
                self.stdout.write(self.style.WARNING('   Skipping token auth (using API key)'))
        except CamPayError as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Authentication failed: {str(e)}'))
            self.stdout.write(self.style.WARNING('\n   Troubleshooting:'))
            self.stdout.write(self.style.WARNING('   1. Verify your username/password in CamPay dashboard'))
            self.stdout.write(self.style.WARNING('   2. Check if your account is activated'))
            self.stdout.write(self.style.WARNING('   3. Confirm BASE_URL is correct for your environment'))
            sys.exit(1)
        
        # Test 3: Phone Number Formatting
        self.stdout.write('\n3. Testing Phone Number Formatting...')
        test_numbers = ['670000000', '237670000000', '6 70 00 00 00']
        
        for num in test_numbers:
            try:
                formatted = campay_service.format_phone_number(num)
                self.stdout.write(f'   {num:20} -> {formatted}')
            except CamPayError as e:
                self.stdout.write(self.style.ERROR(f'   {num:20} -> ERROR: {e}'))
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('✓ CamPay configuration is valid!'))
        self.stdout.write(self.style.SUCCESS('You can now process payments.'))
        self.stdout.write('=' * 70)