from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        if not email:
            raise ValueError(
                'Una dirección de correo electrónico es requerida.'
            )

        user = self.model(
            email=UserManager.normalize_email(email),
            is_active=is_active,
        )
        user.first_name = 'Augusta'
        user.last_name = 'Copropiedades'
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    first_name = models.CharField(
        verbose_name='nombres',
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
    )

    last_name = models.CharField(
        verbose_name='apellidos',
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
    )

    email = models.EmailField(
        verbose_name='correo electrónico',
        unique=True,
        blank=False,
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
    )

    is_active = models.BooleanField(
        'Activo',
        default=True,
    )

    date_joined = models.DateTimeField(
        verbose_name='Fecha de creación',
        default=timezone.now,
    )

    phone_number = models.CharField(
        max_length=128,
        verbose_name='número telefónico',
        default='',
        blank=True,
        validators=[
            MinLengthValidator(6),
        ],
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name='número celular',
        default='',
        blank=True,
    )

    accepted_terms = models.BooleanField(
        verbose_name='aceptar términos y condiciones',
        default=True,
    )

    activation_request_date = models.DateTimeField(
        verbose_name='Fecha de solicitud de activación de cuenta',
        null=True,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name='verificado',
    )

    objects = UserManager()

    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name if self.first_name else self.email.split('@')[0]

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ('last_name',)
