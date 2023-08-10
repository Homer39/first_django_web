from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserRigisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User


class CustomResetConfirmForm(StyleFormMixin, SetPasswordForm):
    class Meta:
        model = User


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(required=True)


