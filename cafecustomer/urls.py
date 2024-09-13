from django.urls import path
from .views import (customer_home, AddToCartAPIView, CartItemsAPIView, CartItemUpdateAPIView)

urlpatterns = [
    path("dashboard/", customer_home, name="customer-home"),
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path('cart/items/', CartItemsAPIView.as_view(), name='cartitems'),
    path('cart/item/<uuid:cartitem_id>/', CartItemUpdateAPIView.as_view(), name='cartitem-detail'), 
]
