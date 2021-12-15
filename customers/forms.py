from django import forms
from .models import Customer, Supplier#, User


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
