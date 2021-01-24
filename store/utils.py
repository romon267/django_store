import json
from .models import *
from django.core.mail import send_mail, mail_admins
import secrets
from datetime import datetime
from django.contrib import messages


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cart_items': cart_items, 'order': order, 'items': items}


# functions decides if user is logged in or a guest and returns his cart items total and items themselves
def process_cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']

    return{'cart_items': cart_items, 'items': items, 'order': order}


def send_order_mails_auth(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    send_mail(
        'Thank you for your order at Django_Store!',
        f'Your order №{order.transaction_id} has been placed and currently being reviewed by managers.\nYou can check your order status in your profile at django_store!',
        'noreply@django_store.com',
        [customer.email]
    )
    mail_admins(
        'New order at django_store',
        f'New order №{order.transaction_id}\n Customer: {customer.name} at {customer.email}'
    )


def send_order_mails_guest(customer, order):

    send_mail(
        'Thank you for your order at Django_Store!',
        f'Your order №{order.transaction_id} has been placed and currently being reviewed by managers.\nYou can check your order status in your profile at django_store!',
        'noreply@django_store.com',
        [customer.email]
    )
    mail_admins(
        'New order at django_store',
        f'New order №{order.transaction_id}\n Customer: {customer.name} at {customer.email}'
    )


def process_order_auth(request, order, form, customer):
    order.complete = True
    order.transaction_id = secrets.token_hex(8)
    order.status = 'Processing by managers.'
    order.date_ordered = datetime.utcnow()
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(customer=customer, order=order, address=form.cleaned_data.get('address'),
                                       city=form.cleaned_data.get('city'), zipcode=form.cleaned_data.get('zipcode'), state=form.cleaned_data.get('state'))
    send_order_mails_auth(request)
    messages.success(request, 'Your order has been placed!')


def process_order_guest(request, form, guest_form, items):
    guest_form.save()
    customer = Customer.objects.create(name=guest_form.cleaned_data.get(
        'name'), email=guest_form.cleaned_data.get('email'))
    db_order = Order.objects.create(customer=customer, complete=True, transaction_id=secrets.token_hex(
        8), status='Processing by managers.')
    for item in items:
        product_id = item['product']['id']
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        OrderItem.objects.get_or_create(
            order=db_order, product=product, quantity=quantity)
    if db_order.shipping == True:
        ShippingAddress.objects.create(customer=customer, order=db_order, address=form.cleaned_data.get('address'),
                                       city=form.cleaned_data.get('city'), zipcode=form.cleaned_data.get('zipcode'), state=form.cleaned_data.get('state'))
    send_order_mails_guest(customer, order=db_order)
    messages.success(request, 'Your order has been placed!')
