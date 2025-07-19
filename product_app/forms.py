from django import forms
from .models import Product, Supplier, Category, StockTransaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'brand' : forms.TextInput(attrs={'class': 'form-control'}),
            'size' : forms.TextInput(attrs={'class': 'form-control'}),
            'color' : forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'stock' : forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier' : forms.Select(attrs={'class': 'form-control'}),
        }
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'phone' : forms.TextInput(attrs={'class': 'form-control'}),
            'address' : forms.Textarea(attrs={'class': 'form-control', 'row': 3}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'})
        }

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = '__all__'
        