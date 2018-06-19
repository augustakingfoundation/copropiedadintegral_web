from hashids import Hashids

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        if not email:
            raise ValueError(
                _('Una dirección de correo electrónico es requerida.')
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
        verbose_name=_('nombres'),
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
    )

    last_name = models.CharField(
        verbose_name=_('apellidos'),
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(3),
        ],
    )

    email = models.EmailField(
        verbose_name=_('correo electrónico'),
        unique=True,
        blank=False,
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('Activo'),
        default=True,
    )

    date_joined = models.DateTimeField(
        verbose_name=_('Fecha de creación'),
        default=timezone.now,
    )

    activation_request_date = models.DateTimeField(
        verbose_name=_('Fecha de solicitud de activación de cuenta'),
        null=True,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('verificado'),
    )

    sent_verification_emails = models.PositiveSmallIntegerField(
        default=0,
    )

    objects = UserManager()

    @property
    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    @property
    def verify_key(self):
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=50)
        return hashids.encode(self.id)

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ('last_name',)
