from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    class Category(models.TextChoices):
        CROISSANTS = 'Croissants', 'Круассаны'
        BREADS = 'Breads', 'Хлеб'
        PASTRIES = 'Pastries', 'Выпечка'
        CAKES = 'Cakes', 'Торты'
        COOKIES = 'Cookies', 'Печенье'
        BUNS = 'Buns', 'Булочки'
    
    product_name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=50, 
        choices=Category.choices,
        default=Category.PASTRIES
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True, null=True)
    seasonal = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    introduced_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cost >= self.price:
            raise ValidationError('Себестоимость должна быть меньше цены')
    
    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'products'
        ordering = ['product_name']
        constraints = [
            models.UniqueConstraint(
                fields=['product_name', 'category'], 
                name='unique_product_in_category'
            )
        ]