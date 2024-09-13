from django.urls import path
from .views import (customer_home, AddToCartAPIView)

urlpatterns = [
    path("dashboard/", customer_home, name="customer-home"),
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
   
]