from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect, render
from store.models import Order, Product, ShippingAddress
from django.core.paginator import Paginator
from .forms import ProductForm


@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    orders = Order.objects.filter(complete=True)
    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save()
            messages.success(request, f'New product № {p.id} has been saved!')
            return redirect('dashboard')
    else:
        form = ProductForm()
    context = {
        'orders': page_obj,
        'form': form,
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
