from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def list(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Продукт не найден'},
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
            product = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Продукт не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Продукт не найден'},
                status=status.HTTP_404_NOT_FOUND
            )