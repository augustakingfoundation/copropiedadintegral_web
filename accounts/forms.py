from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import User


class SignupMixin(forms.Form):
    """
    Signup form mixim. It allows to validate user data
    and save it in the properly format.
    """
    required_css_class = 'required'
    required_fields = [
        'email',
        'first_name',
        'last_name',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.required_fields:
            self.fields[field].required = True

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip().title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip().title()


class SignUpForm(
    SignupMixin,
    UserCreationForm,
):
    """
    Signup Form definition. It inherits from
    the default user creation form of Django.
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


class LoginForm(AuthenticationForm):
    """
    Login form definition. It inherits from
    the default authentication form of Django.
    """
    pass
