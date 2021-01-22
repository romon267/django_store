from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from store.models import Order, ShippingAddress

@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    orders = Order.objects.filter(complete=True)
    context = {
        'orders': orders
    }
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
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

@user_passes_test(lambda u: u.is_staff)
def order_confirm(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'Order was sent to the customer.'
    order.save()

    return redirect('order-detail', pk=pk)