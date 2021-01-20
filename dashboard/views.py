from django.shortcuts import render
from store.models import Order, ShippingAddress

def dashboard(request):
    orders = Order.objects.filter(complete=True)
    context = {
        'orders': orders
    }
    return render(request, 'dashboard/dashboard.html', context)

def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.orderitem_set.all()
    try:
        shipping_address = ShippingAddress.objects.get(order=order)
        context = {
        'order': order,
        'items': items,
        'shipping_address': shipping_address
    }
    except:
        context = {
        'order': order,
        'items': items
    }
    
    return render(request, 'dashboard/order_detail.html', context)