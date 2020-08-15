from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegisterForm
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CustomerForm
from django.contrib import messages
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)

            messages.success(request, f"Your account has been created, Now you can login")
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        "title": "Registeration",
        "form":form
    }
    return render(request, 'users/register.html', context)


@login_required
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    user = request.user
    orders = user.customer.order_set.all()

    context = {
        "title": f"Account - {str(user).title()}",
        "orders": orders,
        "total_orders" : orders.count(),
        "delivered": orders.filter(status='Delivery').count(),
        "pending": orders.filter(status='Pending').count(),
    }
    return render(request, 'users/user.html', context)


@login_required
@allowed_users(allowed_roles=['customer'])
def customerSettings(request):
    form = CustomerForm(instance=request.user.customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request,f"account update")
            return redirect("account")
    context = {
        "title": "Prfile",
        "form": form
    }
    return render(request, 'users/account.html', context)

@login_required
@admin_only
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


@login_required
@allowed_users(allowed_roles=['admin'])
def product(request):
    context = {
        "title": "Product",
        "products" : Product.objects.all()
    }
    return render(request, 'users/product.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def customer(request,id):
    customer = get_object_or_404(Customer, pk=id)
    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        "title": "Customer",
        "customer": customer,
        "orders": orders,
        "myFilter": myFilter
    }
    return render(request, 'users/customer.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
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
        "title": "New Order",
        "formset": form_set
    }
    return render(request, 'users/order_form.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
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
        "title": "Update Order",
        "form": form
    }
    return render(request, 'users/order_form_update.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        order.delete()
        messages.info(request,'Your order has been deleted.')
        return redirect('home')

    context = {
        "title": "Delete Order",
        "order": order
    }

    return render(request, 'users/order_delete.html', context)

