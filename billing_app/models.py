from django.db import models
from product_app.models import Product

# Create your models here.
class Bill(models.Model):
    bill_no = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, blank=True)
    total_amount = models.FloatField()
    
    def __str__(self):
        return self.bill_no

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    
    def subtotal(self):
        return self.quantity * self.price