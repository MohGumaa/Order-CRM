from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from django.contrib import messages

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

def createOrder(request, id):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':
        form_set = orderFormSet(request.POST, instance=customer)
        if form_set.is_valid():
            form_set.save()
            return redirect('home')

    # form = OrderForm(initial={"customer": customer})
    form_set = orderFormSet(queryset=Order.objects.none(), instance=customer)
    context ={
        "formset": form_set
    }
    return render(request, 'users/order_form.html', context)

def updateOrder(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request,'Your order has been updated.')
            return redirect('home')

    else:
        form = OrderForm(instance=order)
    context ={
        "form": form
    }
    return render(request, 'users/order_form.html', context)


def deleteOrder(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        order.delete()
        messages.info(request,'Your order has been deleted.')
        return redirect('home')

    context = {
        "order": order
    }

    return render(request, 'users/order_delete.html', context)
