from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import password_validation

from .models import User


class SignUpForm(UserCreationForm):

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'mobile_number', 'company_name' )
        # field_classes = {'username': UsernameField}


class SignInForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    # email = forms.CharField(
    #     label='Email',
    #     widget=forms.EmailInput(attrs={'class': 'form-control'}),
    # )

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )