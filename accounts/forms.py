from django import forms
from django.forms import Form


class SignUpForm(Form):
    """Formulario de creación de usuarios
    """
    first_name = forms.CharField(
        label='nombres',
        required=True,
        max_length=50,
    )

    last_name = forms.CharField(
        label='apellidos',
        required=True,
        max_length=50,
    )

    email = forms.EmailField(
        label='correo electrónico',
        required=True,
        max_length=50,
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label='contraseña',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label
