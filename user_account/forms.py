from typing import Any
from django import forms
from django.utils.translation import gettext_lazy
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
# from django.db.models import Q
from .models import NormalUser


class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(NormalUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = NormalUser._default_manager.get_by_natural_key(username)
        except NormalUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            NormalUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "autofocus": True}))
    # username = UsernameField(widget=forms.TextInput(attrs={"placeholder": "Username", "autofocus": True}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "autofocus": True}))
    password = forms.CharField(
    label = gettext_lazy("Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}),
    )
    
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.username_field = NormalUser._meta.get_field(NormalUser.USERNAME_FIELD)
        self.auth_n = CustomAuth()

    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = self.auth_n.authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

# class SignUpForm(UserCreationForm):
#     ...