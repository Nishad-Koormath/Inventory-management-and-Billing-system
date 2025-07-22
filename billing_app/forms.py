from django import forms
from .models import Bill, BillItem
from product_app.models import Product

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name']
        
    
class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['product', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].empty_label = 'select product'
        self.fields['quantity'].widget.attrs.update({'min': 1})