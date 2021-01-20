from store.forms import ShippingForm
from django.shortcuts import redirect, render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json
from django.contrib import messages
import random
import secrets

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

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
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
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
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items, 'form': form}
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
