from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def list(self, request):
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            customer = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Клиент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            customer = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(customer, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Клиент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, request, pk=None):
        try:
            customer = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Клиент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )