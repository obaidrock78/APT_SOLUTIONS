from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from auth_email_verify.app_permissions import AppPermission

from saas_web_app.persistance import BaseModel

# Create your models here.

class AuthRole(BaseModel['AuthRole']):
    name = models.CharField(max_length=150)
    permission_objs: models.Manager['RolePermission']

    def flat_permissions_list(self):
        return list(self.permission_objs.values_list('perm_slug', flat=True).all())

    def give_permission(self, permission: AppPermission):
        if not permission.slug in self.flat_permissions_list():
            # rperm = RolePermission()
            RolePermission.objects.create(
                role = self,
                perm_slug = permission.slug
            )
            # rperm.save()


    def remove_permission(self, permission: AppPermission):
        RolePermission.objects.filter(role=self, perm_slug=permission.slug).delete()

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
    pass

class Profile(BaseModel['Profile']):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)