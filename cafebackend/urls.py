
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/account/", include('account.urls')),
    path("api/customer/", include('cafecustomer.urls')),
    path("api/cafeadmin/", include('cafeadmin.urls')),
]
