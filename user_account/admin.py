from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as CreateForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from .models import NormalUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(
                                label="",
                                widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                # help_text= password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Password Confirm"}),
        strip=False,
        # help_text= gettext_lazy("Enter the same password as before, for verification."),
    )

    class Meta:
        model = NormalUser
        fields = ["email", "date_of_birth"]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "date_of_birth": forms.DateTimeInput(attrs={"placeholder": "Date of birth"}),
        }
        labels = {
            "email": "",
            "date_of_birth": "",
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        # print(f"password1: {password1}")
        password2 = self.cleaned_data.get("password2")
        # print(f"password2: {password2}")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    # def clean(self) -> dict[str, Any]:
    #     return self.clean_password2()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NormalUser
        fields = ["email", "password", "date_of_birth", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "date_of_birth", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(NormalUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

# Register your models here.
