
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserChangeForm, CustomUserCreationForm


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'second_name','phone_num')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',
                                       )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'phone_num')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('id','email', 'first_name', 'second_name', 'is_active','is_superuser','phone_num')
    list_filter = ( 'is_superuser', 'is_active')
    search_fields = ('first_name', 'second_name','username', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)
class CNSInline(admin.TabularInline):
    model = CNS
    extra = 1
class CNSImageInline(admin.TabularInline):
    model = CNSImage
    extra = 1
class CNSExtraInline(admin.TabularInline):
    model = CNSExtraField
    extra = 1
class CNSAdmin(admin.ModelAdmin):
    inlines = [ CNSImageInline,CNSExtraInline,]
    list_display = ('id','CHtitle','full_address','district',)
class CNSSpecialAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(CNS,CNSAdmin)
admin.site.register(CNSExtraField)
admin.site.register(CNSSpecialField,CNSSpecialAdmin)
