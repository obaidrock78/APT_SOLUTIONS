from django import forms
from .models import Customer, ServiceItem, Supplier#, User


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = "__all__"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"


class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = "__all__"