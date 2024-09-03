from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import CustomUser                                                                                                                                          


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields':('role',)}),
        )

    list_display = [
            'id',
            'username', 
            'email',
            'role'
        ]

admin.site.register(User, CustomUserAdmin)
