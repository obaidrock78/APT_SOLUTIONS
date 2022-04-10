from django import forms
from .models import Contact, Customer, Note, ServiceItem, Supplier


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = "__all__"


class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['parent']

class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['parent']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['company']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        exclude = ['company']


class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = "__all__"
        exclude = ['company']