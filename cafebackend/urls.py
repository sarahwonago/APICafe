
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cafeteria Management System API",
        default_version='v1',
        description="API documentation for the Cafeteria Management System",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # for obtaining access and refresh token pair
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    # for obtaining refresh token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("api/account/", include('account.urls')),
    path("api/customer/", include('cafecustomer.urls')),
    path("api/cafeadmin/", include('cafeadmin.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]





   
