
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),

    # for obtaining access and refresh token pair
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    # for obtaining refresh token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("api/account/", include('account.urls')),
    path("api/customer/", include('cafecustomer.urls')),
    path("api/cafeadmin/", include('cafeadmin.urls')),

    # schema, redoc docs, swagger ui
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





   
