from django.core import paginator
from store.models import Order, ShippingAddress
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from store.forms import GuestForm

def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created, you are able to login now!')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer = customer, complete = True)
    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)
    cart_items = order.get_cart_items
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            customer.name = form.cleaned_data.get('name')
            customer.email = form.cleaned_data.get('email')
            customer.save()
            messages.success(request, f'Your data has been changed!')
            return redirect('profile')
    else:
        form = GuestForm(instance= request.user.customer)
    context = {'orders': page_obj, 'cart_items': cart_items, 'form': form}
    return render(request, 'users/profile.html', context)

@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.orderitem_set.all()
    customer = request.user.customer
    cart_order, created = Order.objects.get_or_create(customer = customer, complete=False)
    cart_items = cart_order.get_cart_items
    try:
        shipping_address = ShippingAddress.objects.get(order=order)
        context = {
        'order': order,
        'items': items,
        'shipping_address': shipping_address,
        'cart_items': cart_items,
    }
    except:
        context = {
        'order': order,
        'items': items,
        'cart_items': cart_items,
    }
    
    return render(request, 'users/order_detail.html', context)