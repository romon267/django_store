from django.urls import path
from . import views as dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
    path('order_detail/<int:pk>/', dashboard_views.order_detail, name='order-detail')
]
