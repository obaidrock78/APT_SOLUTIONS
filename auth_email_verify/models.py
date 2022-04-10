from typing import Optional, Iterable

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_email_verify.app_permissions import AppPermission
from saas_web_app.persistance import BaseModel

# Create your models here.

class AuthRole(BaseModel['AuthRole']):

    class RlType:
        BASIC = 'basic' # = built-in
        USER_DEFINED = 'user-defined'
        
    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150, default='other')
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
            self.wrap_permission_object(permission).save()

    def wrap_permission_object(self, permission: AppPermission):
        perm = RolePermission()
        perm.role = self
        perm.perm_slug = permission.slug

        return perm

    def remove_permission(self, permission: AppPermission):
        RolePermission.objects.filter(role=self, perm_slug=permission.slug).delete()

    def has_permission(self, perm_slug: str):
        return perm_slug in self.flat_permissions_list()

    def give_permissions_bulk(self, permissions: Iterable[AppPermission]):
        p_objs = [
            self.wrap_permission_object(p)
            for p in permissions
            if not self.has_permission(p.slug)
        ]
        RolePermission.objects.bulk_create(p_objs)

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
    company = models.OneToOneField('customers.Company', on_delete=models.CASCADE, related_name="owner", null=True)

    @property
    def get_clients(self):
        try:
            return self.company.clients.all()
        except:
            return None

    @property
    def get_customers(self):
        try:
            return self.company.customers.all()
        except:
            return None

    @property
    def get_service_items(self):
        try:
            return self.company.service_items.all()
        except:
            return None

    @property
    def get_team_members(self):
        try:
            return self.company.team_members.all()
        except:
            return None

    @property
    def get_suppliers(self):
        try:
            return self.company.suppliers.all()
        except:
            return None
    
class Profile(BaseModel['Profile']):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)

class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="team_members")
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)




@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()