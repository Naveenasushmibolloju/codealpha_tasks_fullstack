from django.urls import path
from django.urls import path
from .views import (
    home,
    product_detail,
    add_to_cart,
    remove_from_cart,
    cart,
    checkout,
    register,
    order_history
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('orders/', order_history, name='orders'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
]