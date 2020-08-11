from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    context = {
        "title": "Home",
        "orders" : orders,
        "customers": customers,
        "total_customer": customers.count(),
        "total_orders" : orders.count(),
        "delivered": orders.filter(status='Delivery').count(),
        "pending": orders.filter(status='Pending').count(),
    }
    return render(request, 'users/dashboard.html', context)

def product(request):
    context = {
        "title": "Product",
        "products" : Product.objects.all()
    }
    return render(request, 'users/product.html', context)

def customer(request,id):
    customer = get_object_or_404(Customer, pk=id)
    context = {
        "title": "Customer",
        "customer": customer,
        "orders": customer.order_set.all()
    }
    return render(request, 'users/customer.html', context)
