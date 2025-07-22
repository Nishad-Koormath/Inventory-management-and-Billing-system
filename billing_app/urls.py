from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_bill, name='create_bill'),
    path('list/', views.bill_list, name='bill_list'),
    path('bill/<int:pk>/', views.bill_detail, name='bill_detail'),
]