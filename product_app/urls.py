from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_add, name='product_add'),
    path('edit/<int:pk>', views.product_edit, name='product_edit'),
    path('delete/<int:pk>', views.product_delete, name='product_delete'),
    
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>', views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>', views.supplier_delete, name='supplier_delete'),
    
    path('category/', views.category_list, name='category_list'),
    path('category/add', views.category_add, name='category_add'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    path('stock/', views.stock_transaction, name='stock_transaction'),
    path('stock/history', views.stock_transaction_list, name='stock_transaction_list'),
    path('stock-report/', views.stock_report, name='stock_report'),
]