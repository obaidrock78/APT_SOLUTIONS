from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Profile, AuthRole, RolePermission, User


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'verify']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_filter = ['role']


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Additional Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                    'company',
                ),
            },
        ),
    )

admin.site.register(AuthRole)
admin.site.register(User, CustomUserAdmin)
