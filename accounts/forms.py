from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm

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


class UserPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        return (u for u in active_users)


class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña actual',
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Nueva contraseña',
        required=False,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar nueva contraseña',
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'current_password',
            'new_password',
            'password_confirm',
        ]

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        password_confirm = cleaned_data.get('password_confirm')
        user = getattr(self, 'instance', None)

        if (
            (current_password or new_password) and
            not user.check_password(current_password)
        ):
            self.add_error(
                'current_password',
                'Contraseña no válida.',
            )

        if new_password != password_confirm:
            self.add_error(
                'password_confirm',
                'Las contraseñas no coinciden.',
            )

        return cleaned_data
