from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('order/<str:order_number>/print-label/', views.print_delivery_label, name='print_delivery_label'),
    path('order/<str:order_number>/print-receipt/', views.print_customer_receipt, name='print_customer_receipt'),
]
