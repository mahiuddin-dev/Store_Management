from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from account.models import User


# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'address', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', )}),
        ('Personal', {'fields': ('last_login', 'date_joined', 'unique_id', 'first_name', 'last_name', 'phone_number', 'address', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(User, UserAdminConfig)
