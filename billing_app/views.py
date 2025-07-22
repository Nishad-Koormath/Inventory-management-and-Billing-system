from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Bill, BillItem
from .forms import BillForm, BillItemForm 
from django.utils.crypto import get_random_string
from inventory_app.models import StockTransaction

# Create your views here.
def create_bill(request):
    BillItemFormSet = modelformset_factory(BillItem, form=BillItemForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        formset = BillItemFormSet(request.POST, queryset=BillItem.objects.none())
        
        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save(commit=False)
            bill.bill_no = "BILL" + get_random_string(5).upper()
            bill.total_amount = 0
            bill.save()
            
            for form in formset:
                if form.cleaned_data:
                    item = form.save(commit=False)
                    item.bill = bill
                    item.price = item.product.sales_price
                    item.save()
                    
                    #reduce stock 
                    item.product.stock -= item.quantity
                    item.product.save()
                
                    #log_stock_out
                    StockTransaction.objects.create(
                        product = item.product,
                        quantity = item.quantity,
                        transaction_types = 'OUT',
                        remarks = f"Billed via {bill.bill_no}" 
                    )
                
                    bill.total_amount += item.quantity * item.price
                
            bill.save()
            return redirect('bill_detail', pk=bill.pk)
    else:
        bill_form = BillForm()
        formset = BillItemFormSet(queryset=BillItem.objects.none())
        
    return render(request, 'billing_app/create_bill.html', {
        'bill_form': bill_form,
        'formset': formset
    })
    
def bill_list(request):
    bills = Bill.objects.all().order_by('-created_at')
    return render(request, 'billing_app/bill_list.html', {'bills': bills})
    
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    bill_items = bill.items.all()
    
    return render(request, 'billing_app/billing_detail.html', {
        'bill': bill,
        'items': bill_items,
    })