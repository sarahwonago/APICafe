from django.urls import path
from .views import customer_home

urlpatterns = [
    path("dashboard/", customer_home, name="customer-home"),
   
]