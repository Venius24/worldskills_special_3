from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def validate_email(self, value):
        # Проверка уникальности email при обновлении
        if self.instance:
            if Customer.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("Клиент с таким email уже существует")
        else:
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("Клиент с таким email уже существует")
        return value