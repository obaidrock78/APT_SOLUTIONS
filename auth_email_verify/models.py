from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from auth_email_verify.app_permissions import AppPermission

from saas_web_app.persistance import BaseModel

# Create your models here.

class AuthRole(BaseModel['AuthRole']):

    class RlType:
        BASIC = 'basic' # = built-in
        USER_DEFINED = 'user-defined'
        
    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150, default='other')
    is_default = models.BooleanField(default=False)
    rltype = models.CharField(
        max_length=20, 
        choices=(
            (RlType.BASIC,          "Basic"),
            (RlType.USER_DEFINED,   "User Defined"),
        )
    )

    permission_objs: models.Manager['RolePermission']

    def flat_permissions_list(self):
        return list(self.permission_objs.values_list('perm_slug', flat=True).all())

    def give_permission(self, permission: AppPermission):
        if not permission.slug in self.flat_permissions_list():
            RolePermission.objects.create(
                role=self,
                perm_slug=permission.slug
            )

    def remove_permission(self, permission: AppPermission):
        RolePermission.objects.filter(role=self, perm_slug=permission.slug).delete()

    def has_permission(self, perm_slug: str):
        return perm_slug in self.flat_permissions_list()

    def __str__(self):
        return self.name


class RolePermission(BaseModel['RolePermission']):
    role_id: int
    role = models.ForeignKey(
        AuthRole,
        db_column='role_id',
        related_name='permission_objs',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    perm_slug = models.CharField(max_length=100)

    def __str__(self):
        return self.perm_slug


class User(AbstractUser):
    role_id: Optional[int]
    role = models.ForeignKey(
        AuthRole,
        db_column='role_id',
        related_name='assigned_users',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

class Profile(BaseModel['Profile']):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)