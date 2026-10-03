from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from customers.models import Customer
from products.models import Product
from .models import Order


class OrderApiTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Test', last_name='Customer', email='test@example.com'
        )
        self.product = Product.objects.create(
            product_name='Croissant', price=Decimal('3.50'), cost=Decimal('1.00'),
            introduced_date=date(2024, 1, 1),
        )
        self.client = APIClient()

    def test_order_requires_authentication(self):
        self.assertEqual(self.client.post('/api/orders/', {}, format='json').status_code, 401)

    def test_create_order_uses_catalog_price_and_blocks_direct_edits(self):
        self.client.force_authenticate(user=get_user_model().objects.create_user(username='staff'))
        response = self.client.post('/api/orders/', {
            'customer': self.customer.pk,
            'items': [{'product': self.product.pk, 'quantity': 2, 'price': '0.01'}],
        }, format='json')
        self.assertEqual(response.status_code, 201)
        order = Order.objects.get()
        self.assertEqual(order.total_amount, Decimal('7.00'))
        self.assertEqual(order.items.get().price, Decimal('3.50'))
        self.assertEqual(self.client.patch(f'/api/orders/{order.pk}/', {'total_amount': '0.01'}, format='json').status_code, 405)
        self.assertEqual(self.client.delete(f'/api/orders/{order.pk}/').status_code, 405)

    def test_invalid_quantity_does_not_create_order(self):
        self.client.force_authenticate(user=get_user_model().objects.create_user(username='staff'))
        response = self.client.post('/api/orders/', {
            'customer': self.customer.pk,
            'items': [{'product': self.product.pk, 'quantity': 0}],
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Order.objects.exists())
