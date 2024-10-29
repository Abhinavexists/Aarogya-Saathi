# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password should be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password should contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password should contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password should contain at least one number.")
        if not re.search(r'[@$!%*?&#]', password):
            raise ValidationError("Password should contain at least one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
