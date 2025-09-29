import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.menu.models import MenuItem, MenuCategory

class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass', role='canteen_admin')
        self.client.login(username='admin', password='pass')
        self.category = MenuCategory.objects.create(name='Test Cat')

    def test_menu_management_view(self):
        MenuItem.objects.create(name='Item1', price=Decimal('5.00'), category=self.category)
        response = self.client.get(reverse('menu:management') + '?status=available')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item1')

    def test_add_menu_item_json(self):
        data = json.dumps({
            'name': 'New Item', 'price': '10.00', 'category': str(self.category.id),
            'description': 'Test', 'prep_time': 15, 'current_stock': 100
        })
        response = self.client.post(reverse('menu:add_item'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content['success'])
        item = MenuItem.objects.latest('id')
        self.assertEqual(item.name, 'New Item')

    def test_update_menu_item_json(self):
        item = MenuItem.objects.create(name='Old', price=Decimal('5.00'), category=self.category)
        data = json.dumps({'name': 'Updated', 'price': '15.00'})
        response = self.client.post(reverse('menu:update_item', args=[item.id]), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Updated')

# Run with: python manage.py test menu