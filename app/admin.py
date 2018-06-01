
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserChangeForm, CustomUserCreationForm


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','phone_num')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_num')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'second_name', 'is_superuser','phone_num')
    list_filter = ( 'is_superuser', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)
admin.site.register(CustomUser, UserAdmin)
