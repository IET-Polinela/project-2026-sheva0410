from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'is_admin', 'is_member', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_admin', 'is_member')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('is_admin', 'is_member')
        }),
    )


admin.site.register(User, CustomUserAdmin)