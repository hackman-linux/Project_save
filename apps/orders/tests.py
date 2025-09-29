import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.menu.models import MenuItem
from apps.orders.models import Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='employee', password='pass', role='employee')
        self.client.login(username='employee', password='pass')
        self.menu_item = MenuItem.objects.create(name='Test Item', price=Decimal('10.00'))

    def test_place_order_success(self):
        data = {
            'full_name': 'Test User', 'email': 'test@email.com', 'phone_number': '123',
            'office_number': '101', 'special_instructions': 'None',
            f'item_{self.menu_item.id}': 2  # Quantity
        }
        response = self.client.post(reverse('orders:place_order'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect to history
        order = Order.objects.latest('id')
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('20.00'))
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_place_order_no_items_json(self):
        data = json.dumps({'full_name': 'Test', 'email': 'test@email.com'})  # No items
        response = self.client.post(reverse('orders:place_order'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Redirect with error
        self.assertFalse(Order.objects.exists())  # Rolled back

    def test_place_order_invalid_quantity(self):
        data = {f'item_{self.menu_item.id}': -1}  # Invalid qty
        response = self.client.post(reverse('orders:place_order'), data=data)
        self.assertEqual(response.status_code, 302)  # Should handle gracefully (no item created)

    # Continuing from above OrderTests class

    def test_orders_management_filter(self):
        # Create sample order
        order = Order.objects.create(employee=self.user, status='pending', total_amount=Decimal('10.00'))
        self.admin = User.objects.create_user(username='admin', password='pass', role='canteen_admin')
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('orders:management') + '?status=pending')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)  # Check in template

    def test_confirm_order_json(self):
        order = Order.objects.create(employee=self.user, status='pending')
        data = json.dumps({'status': 'validated'})  # Simulate AJAX POST
        response = self.client.post(reverse('orders:confirm', args=[order.id]), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'validated')
        content = json.loads(response.content)
        self.assertTrue(content['success'])

    def test_cancel_order(self):
        order = Order.objects.create(employee=self.user, status='pending')
        response = self.client.post(reverse('orders:cancel', args=[order.id]))
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

# Run with: python manage.py test orders