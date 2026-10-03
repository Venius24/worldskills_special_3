from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from django.db import transaction

class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all().prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def list(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        """Завершить заказ по идентификатору"""
        try:
            order = self.get_queryset().get(pk=pk)
            
            if order.status == 'Completed':
                return Response(
                    {'error': 'Заказ уже завершен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if order.status == 'Cancelled':
                return Response(
                    {'error': 'Невозможно завершить отмененный заказ'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = 'Completed'
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        """Отменить заказ по идентификатору"""
        try:
            order = self.get_queryset().get(pk=pk)
            
            if order.status == 'Completed':
                return Response(
                    {'error': 'Невозможно отменить завершенный заказ'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if order.status == 'Cancelled':
                return Response(
                    {'error': 'Заказ уже отменен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = 'Cancelled'
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['put'])
    def process(self, request, pk=None):
        """Перевести заказ в статус Processing"""
        try:
            order = self.get_queryset().get(pk=pk)
            
            if order.status != 'Pending':
                return Response(
                    {'error': 'Можно обработать только заказы со статусом Pending'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = 'Processing'
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
