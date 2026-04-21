from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.core.exceptions import ValidationError
import re

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        label="Username",
        help_text="Letters, numbers, and spaces are allowed.",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not re.match(r'^[a-zA-Z0-9 ]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and spaces.")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
            
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['license_number', 'age']