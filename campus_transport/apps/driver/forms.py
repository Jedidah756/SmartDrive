from django import forms
from django.contrib.auth import authenticate


class DriverLoginForm(forms.Form):
    email = forms.EmailField(label="Driver Email", widget=forms.EmailInput(attrs={"placeholder": "driver@campus.local"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if not self.user:
                raise forms.ValidationError("Invalid email or password.")
            if not getattr(self.user, "is_driver", False):
                raise forms.ValidationError("This account is not registered as a driver.")
        return cleaned_data

    def get_user(self):
        return self.user

