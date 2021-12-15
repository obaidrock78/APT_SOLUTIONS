from django.contrib import admin
from .models import Company, Customer, Supplier, Client#, User

# Register your models here.

# admin.site.register(User)
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Client)