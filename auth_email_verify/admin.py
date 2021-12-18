from django.contrib import admin
from . models import Profile, AuthRole, RolePermission

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'verify']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_filter = ['role']

admin.site.register(AuthRole)
