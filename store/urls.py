from django.urls import path
from . import views as store_views

urlpatterns = [
    path('', store_views.store, name="home"),
    path('store/', store_views.store, name="store"),
    path('cart/', store_views.cart, name="cart"),
    path('checkout/', store_views.checkout, name="checkout"),
    path('update_item/', store_views.updateItem, name="update_item"),
    path('product-detail/<int:pk>', store_views.product_detail, name='product-detail'),
    path('product-delete/<int:pk>', store_views.delete_product, name='delete-product')
]