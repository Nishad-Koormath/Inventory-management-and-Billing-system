from django.db import models
from django.core.exceptions import ValidationError
from product_app.models import Product

# Create your models here.
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