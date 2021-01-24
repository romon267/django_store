from store.forms import ShippingForm, GuestForm
from django.shortcuts import redirect, render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json
from django.contrib import messages
import secrets
from .utils import cookieCart, process_cart_items, process_order_auth, process_order_guest
from datetime import datetime
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.decorators import user_passes_test

def store(request):
    # displaying cart total in the navbar
    cart_data = process_cart_items(request)
    cart_items = cart_data['cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}

    return render(request, 'store/store.html', context)


def product_detail(request, pk):
    # displaying cart total in the navbar
    cart_data = process_cart_items(request)
    cart_items = cart_data['cart_items']
    product = Product.objects.get(pk=pk)
    context = {'product': product, 'cart_items': cart_items}

    return render(request, 'store/product_detail.html', context)


def cart(request):
    # getting cart items total and item list from the function
    cart_data = process_cart_items(request)
    items = cart_data['items']
    cart_items = cart_data['cart_items']
    order = cart_data['order']
    context = {'items': items, 'order': order, 'cart_items': cart_items}

    return render(request, 'store/cart.html', context)


def checkout(request):
    guest_form = GuestForm()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        if request.method == "POST":
            form = ShippingForm(request.POST)
            if form.is_valid():
                form.save()
                process_order_auth(request, order, form, customer)
                return redirect('home')
            elif order.shipping == False:
                process_order_auth(request, order, form, customer)
                return redirect('home')
        else:
            form = ShippingForm()
    else:
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']
        if request.method == "POST":
            form = ShippingForm(request.POST)
            guest_form = GuestForm(request.POST)
            if form.is_valid() and guest_form.is_valid():
                form.save()
                process_order_guest(request, form, guest_form, items)
                return redirect('home')
            elif guest_form.is_valid() and order['shipping'] == False:
                process_order_guest(request, form, guest_form, items)
                return redirect('home')
        else:
            form = ShippingForm()
            guest_form = GuestForm()

    context = {'items': items, 'order': order,
               'cart_items': cart_items, 'form': form, 'guest_form': guest_form}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    messages.success(request, 'Product was deleted!')
    return redirect('store')