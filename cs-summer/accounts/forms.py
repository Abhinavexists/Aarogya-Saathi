# accounts/forms.py
from django import forms
from .models import UserProfile  # Import the UserProfile model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
import re

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserProfile  # Use the UserProfile model
        fields = ['full_name', 'email', 'password']  # Include full_name in fields

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

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError("Invalid email or password.")
        return cleaned_data
