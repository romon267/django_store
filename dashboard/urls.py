from django.urls import path
from . import views as dashboard_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
    path('order_detail/<int:pk>/', dashboard_views.order_detail, name='order-detail'),
    path('order_confirm/<int:pk>/', dashboard_views.order_confirm, name='order-confirm')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
