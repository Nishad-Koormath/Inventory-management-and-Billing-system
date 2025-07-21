from django.urls import path
from . import views

urlpatterns = [   
    path('stock/', views.stock_transaction, name='stock_transaction'),
    path('stock/history', views.stock_transaction_list, name='stock_transaction_list'),
    path('stock-report/', views.stock_report, name='stock_report'),
]