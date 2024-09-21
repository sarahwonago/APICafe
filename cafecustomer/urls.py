from django.urls import path
from .views import (customer_home, AddToCartAPIView, CartItemsAPIView, CartItemUpdateAPIView,
                    CreateOrderAPIView, PaymentAPIView, OrderHistoryAPIView,
                    ReviewAPIView, CustomerPointAPIView, CustomerRedeemPointAPIView)

urlpatterns = [
    path("dashboard/", customer_home, name="customer-home"),
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path('cart/items/', CartItemsAPIView.as_view(), name='cartitems'),
    path('cart/item/<uuid:cartitem_id>/', CartItemUpdateAPIView.as_view(), name='cartitem-detail'), 
    path("create-order/", CreateOrderAPIView.as_view(),name="create-order"),
    path("make-payment/", PaymentAPIView.as_view(), name="make-payment"),
    path("order-history/", OrderHistoryAPIView.as_view(), name="order-history"),
    path("review/", ReviewAPIView.as_view(), name="list-create-review"),
    path("customer-points/", CustomerPointAPIView.as_view(), name="customer-points"),
    path("redeem-points/<uuid:pk>/", CustomerRedeemPointAPIView.as_view(), name="redeem-points"),
]
