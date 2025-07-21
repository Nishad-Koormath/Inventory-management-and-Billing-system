from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Supplier, Category, StockTransaction
from .forms import ProductForm, SupplierForm, CategoryForm, StockTransactionForm
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.db.models import Sum

# Create your views here.
# product
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_app/product_list.html', {'products' : products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
        return render(request, 'product_app/product_form.html', {'form' : form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        return render(request, 'product_app/product_form.html', {'form':form})
    
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_app/product_confirm_delete.html', {'product' : product})


# supplier
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'product_app/supplier_list.html', {'suppliers': suppliers})

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'product_app/supplier_form.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'product_app/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'product_app/supplier_confirm_delete.html', {'supplier': supplier})


# category
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'product_app/category_list.html', {"categories": categories})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
        return render(request, 'product_app/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product_app/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'product_app/category_confirm_delete.html')


# stock
def stock_transaction(request):
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('product_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = StockTransactionForm()
    return render(request, 'product_app/stock_transaction.html', {'form': form})

def stock_transaction_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    transactions = StockTransaction.objects.select_related('product').order_by('-timestamp')
    
    product_id = request.GET.get('product')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if category_id:
        transactions = transactions.filter(product__category__id=category_id)
    if product_id:
        transactions = transactions.filter(product__id = product_id )
    if start_date:
        transactions = transactions.filter(timestamp__date__gte=parse_date(start_date))
    if end_date:
        transactions = transactions.filter(timestamp__date__lte=parse_date(end_date))
        
    total_in = transactions.filter(transaction_types = 'IN').aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_out = transactions.filter(transaction_types = 'OUT').aggregate(Sum('quantity'))['quantity__sum'] or 0
    
        
    return render(request, 'product_app/stock_transaction_list.html', {
        'transactions': transactions,
        'products': products,
        'categories': categories,
        'total_in': total_in,
        'total_out': total_out,
        })
    
    
def stock_report(request):
    products = Product.objects.all()
    report_data = []
    
    for product in products:
        transactions = StockTransaction.objects.filter(product=product).order_by('timestamp')
        
        balance = 0
        product_report = []
        
        for tx in transactions:
            qty_in = tx.quantity if tx.transaction_types == 'IN' else 0
            qty_out = tx.quantity if tx.transaction_types == 'OUT' else 0
            balance += qty_in - qty_out
            
            product_report.append({
                'date': tx.timestamp,
                'product': product.name,
                'in': qty_in,
                'out': qty_out, 
                'balance': balance,
            })
            
        if product_report:
            report_data.extend(product_report)
    return render(request, 'product_app/stock_report.html', {'report_data': report_data})