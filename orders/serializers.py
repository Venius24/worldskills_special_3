from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from customers.serializers import CustomerSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ['id', 'price']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'order_date', 'total_amount', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_date', 'created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['customer', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # 1. Сначала создаем заказ с суммой 0
        order = Order.objects.create(
            customer=validated_data['customer'],
            total_amount=0,
            status='Pending'
        )

        total_amount = 0

        # 2. Создаем позиции, беря цену из модели Product
        for item_data in items_data:
            product = item_data['product']
            price = product.price  # Берем актуальную цену из БД
            quantity = item_data['quantity']

            total_amount += price * quantity

            OrderItem.objects.create(
                order=order, 
                product=product,
                quantity=quantity,
                price=price # Записываем цену на момент покупки
            )

        # 3. Обновляем итоговую сумму заказа
        order.total_amount = total_amount
        order.save()

        return order
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Заказ должен содержать хотя бы одну позицию")
        return value
