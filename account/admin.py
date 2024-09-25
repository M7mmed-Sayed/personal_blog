from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser

class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'gender', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'gender', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(AppUser, AppUserAdmin)
