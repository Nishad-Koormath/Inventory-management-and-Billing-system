from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Product
from inventory_app.models import StockTransaction


@receiver(post_save, sender=Product)
def create_initial_stock_transaction(sender, instance, created, **kwargs):
    if created and instance.stock > 0:
        StockTransaction.objects.create(
            product = instance,
            transaction_types = StockTransaction.IN,
            quantity = instance.stock,
            remarks = 'Initial stock add during product creation.'
        )