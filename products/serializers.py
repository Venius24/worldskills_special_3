from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, data):
        if data.get('cost') and data.get('price'):
            if data['cost'] >= data['price']:
                raise serializers.ValidationError(
                    "Себестоимость должна быть меньше цены"
                )
        return data