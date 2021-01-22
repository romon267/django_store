from store.forms import ShippingForm, GuestForm
from django.shortcuts import redirect, render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json
from django.contrib import messages
import random
import secrets
from .utils import cookieCart

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}

    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        if request.method == "POST":
            form = ShippingForm(request.POST)
            form.save()
            order.complete = True
            order.transaction_id = secrets.token_hex(8)
            order.status = 'Processing by managers.'
            order.save()
            if order.shipping == True:
                ShippingAddress.objects.create(customer=customer, order=order, address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'), zipcode=form.cleaned_data.get('zipcode'), state=form.cleaned_data.get('state'))
            messages.success(request, 'Your order has been placed!')
            return redirect('home')
        else:
            form = ShippingForm()
    else:
        form = ShippingForm()
        guest_form = GuestForm()
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']
        if request.method == "POST":
            form = ShippingForm(request.POST)
            guest_form = GuestForm(request.POST)
            form.save()
            guest_form.save()
            customer = Customer.objects.create(name = guest_form.cleaned_data.get('name'), email = guest_form.cleaned_data.get('email'))

            db_order = Order.objects.create(customer = customer, complete = True, transaction_id = secrets.token_hex(8), status='Processing by managers.')
            for item in items:
                product_id = item['product']['id']
                product = Product.objects.get(id = product_id)
                quantity = item['quantity']
                orderitem, created = OrderItem.objects.get_or_create(order=db_order, product=product, quantity=quantity)
            if db_order.shipping == True:
                ShippingAddress.objects.create(customer=customer, order=db_order, address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'), zipcode=form.cleaned_data.get('zipcode'), state=form.cleaned_data.get('state'))
            messages.success(request, 'Your order has been placed!')
            return redirect('home')
            
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'form': form, 'guest_form': guest_form}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -=1
    
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)
