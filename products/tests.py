from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Product
from datetime import date
import base64

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name='Круассан',
            category='Croissants',
            price=5.50,
            cost=2.00,
            description='Свежий круассан',
            seasonal=False,
            active=True,
            introduced_date=date.today()
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Круассан')
        self.assertEqual(self.product.category, 'Croissants')
        self.assertTrue(self.product.active)
    
    def test_product_str(self):
        self.assertEqual(str(self.product), 'Круассан')

class ProductAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        credentials = base64.b64encode(b'staff:BCLyon2024').decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {credentials}')
        
        self.product_data = {
            'product_name': 'Багет',
            'category': 'Breads',
            'price': 3.50,
            'cost': 1.50,
            'description': 'Французский багет',
            'seasonal': False,
            'active': True,
            'introduced_date': '2024-01-01'
        }
    
    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_product(self):
        response = self.client.post('/api/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_update_product(self):
        product = Product.objects.create(**self.product_data)
        updated_data = self.product_data.copy()
        updated_data['price'] = 4.00
        response = self.client.put(f'/api/products/{product.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(float(product.price), 4.00)
    
    def test_delete_product(self):
        product = Product.objects.create(**self.product_data)
        response = self.client.delete(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)