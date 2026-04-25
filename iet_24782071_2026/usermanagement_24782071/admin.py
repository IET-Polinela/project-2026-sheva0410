from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # TAMPIL DI LIST
    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff', 'is_superuser')

    # TAMPIL DI DETAIL
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_admin', 'is_member')
        }),
    )

    #FORM TAMBAH USER
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('email', 'is_admin', 'is_member')
        }),
    )


admin.site.register(User, CustomUserAdmin)