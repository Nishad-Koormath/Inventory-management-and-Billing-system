from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.size}/{self.color})"
    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class StockTransaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TRANSACTION_TYPES = [
        (IN, 'Stock In'),
        (OUT, 'Stock Out'),
    ]
    
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_types = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=300, blank=True)
    
    def save(self, *args, **kwargs):
        if self.transaction_types == self.IN:
            self.product.stock += self.quantity
        elif self.transaction_types == self.OUT:
            if self.product.stock < self.quantity:
                raise ValidationError('Not enough stock to perform this transaction.')
            self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
