from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from .data import BUILDING_DOCUMENT_TYPE_CHOICES
from accounts.data import DOCUMENT_TYPE_CHOICES
from app.validators import FileSizeValidator


class BuildingMembership(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name='usuario',
    )

    building = models.ForeignKey(
        'buildings.Building',
        on_delete=models.CASCADE,
        verbose_name='copropiedad',
    )

    is_administrator = models.BooleanField(
        verbose_name='administrador',
        default=False,
    )

    is_administrative_assistant = models.BooleanField(
        verbose_name='asistente administrativo',
        default=False,
    )

    is_accountant = models.BooleanField(
        verbose_name='contador',
        default=False,
    )

    is_accounting_assistant = models.BooleanField(
        verbose_name='asistente contable',
        default=False,
    )

    is_fiscal_reviewer = models.BooleanField(
        verbose_name='revisor fiscal',
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name='membresía activa',
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.user,
            self.building
        )

    class Meta:
        verbose_name = 'membresía'
        verbose_name_plural = 'membresías'
        ordering = ('created_at',)
        unique_together = (
            ('user', 'building'),
        )


class Building(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='nombre',
    )

    document_type = models.PositiveSmallIntegerField(
        choices=BUILDING_DOCUMENT_TYPE_CHOICES,
        verbose_name='tipo de documento',
    )

    document_number = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='documento/Nit',
    )

    logo = models.ImageField(
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    city = models.ForeignKey(
        'place.City',
        verbose_name='ciudad',
        on_delete=models.DO_NOTHING,
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='dirección',
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='correo electrónico',
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name='número celular',
        default='',
        blank=True,
        help_text='Si desea ingresar más de un número celular,'
                ' estos deben ir separados por coma (,).',
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo debe ingresar números.'
                        ' Si desea ingresar más de un número celular, estos '
                        'deben estar separados por coma (,).'
            ),
            MinLengthValidator(10),
        ],
        error_messages={
            'min_length':
                'Ingrese al menos %(limit_value)d caracteres,'
                ' (actualmente tiene %(show_value)d).'
        }
    )

    phone_number = models.CharField(
        max_length=32,
        verbose_name='número telefónico',
        help_text='Si desea ingresar más de un número telefónico,'
                  ' estos deben ir separados por coma (,).',
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo se permiten números.'
                        ' Si desea ingresar más de un número telefónico,'
                        ' estos deben estar separados por coma (,).'
            ),
            MinLengthValidator(6),
        ],
        error_messages={
            'min_length':
                'El campo "Número telefónico" debe tener al menos '
                '%(limit_value)d dígitos (actualmente tiene %(show_value)d).'
        }
    )

    initial_period = models.DateField(
        blank=True,
        null=True,
        verbose_name='periodo inicial',
    )

    activity_log = models.TextField(
        blank=True,
        verbose_name='registro de actividad',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def get_absolute_url(self):
        return reverse(
            'buildings:building_detail', args=[self.id]
        )

    def __str__(self):
        return '{0} - {1}'.format(
            self.name,
            self.document_number,
        )

    class Meta:
        verbose_name = 'copropiedad'
        verbose_name_plural = 'copropiedades'
        ordering = ('created_at',)


class Unit(models.Model):
    building = models.ForeignKey(
        'buildings.Building',
        on_delete=models.CASCADE,
        verbose_name='copropiedad',
    )

    block = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='bloque',
        help_text='Bloque o interior',
    )

    unit = models.CharField(
        max_length=50,
        verbose_name='unidad',
        help_text='apartamento, casa u oficina',
    )

    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='área (Mts)',
    )

    real_estate_registration = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='matrícula inmobiliaria',
    )

    owner_name = models.CharField(
        max_length=100,
        verbose_name='nombre del propietario',
    )

    owner_document_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name='tipo de documento del propietario',
    )

    owner_document_number = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name='número de documento del propietario',
    )

    owner_mobile_phone = models.CharField(
        max_length=32,
        verbose_name='número celular del propietario',
        default='',
        blank=True,
        help_text='Si desea ingresar más de un número celular,'
                ' estos deben ir separados por coma (,).',
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo debe ingresar números.'
                        ' Si desea ingresar más de un número celular, estos '
                        'deben estar separados por coma (,).'
            ),
            MinLengthValidator(10),
        ],
        error_messages={
            'min_length':
                'Ingrese al menos %(limit_value)d caracteres,'
                ' (actualmente tiene %(show_value)d).'
        }
    )

    owner_phone_number = models.CharField(
        max_length=32,
        verbose_name='número telefónico del propietario',
        help_text='Si desea ingresar más de un número telefónico,'
                  ' estos deben ir separados por coma (,).',
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo se permiten números.'
                        ' Si desea ingresar más de un número telefónico,'
                        ' estos deben estar separados por coma (,).'
            ),
            MinLengthValidator(6),
        ],
        error_messages={
            'min_length':
                'El campo "Número telefónico" debe tener al menos '
                '%(limit_value)d dígitos (actualmente tiene %(show_value)d).'
        }
    )

    owner_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='correo electrónico del propietario',
    )

    correspondence_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='dirección de correspondencia',
        help_text='dirección alternativa para enviar correspondencia'
                  ' al propietario de la unidad',
    )

    leaseholder_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='nombre del arrendatario',
    )

    leaseholder_mobile_phone = models.CharField(
        max_length=32,
        verbose_name='número celular del arrendatario',
        default='',
        blank=True,
        help_text='Si desea ingresar más de un número celular,'
                ' estos deben ir separados por coma (,).',
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo debe ingresar números.'
                        ' Si desea ingresar más de un número celular, estos '
                        'deben estar separados por coma (,).'
            ),
            MinLengthValidator(10),
        ],
        error_messages={
            'min_length':
                'Ingrese al menos %(limit_value)d caracteres,'
                ' (actualmente tiene %(show_value)d).'
        }
    )

    leaseholder_phone_number = models.CharField(
        max_length=32,
        verbose_name='número telefónico del arrendatario',
        help_text='Si desea ingresar más de un número telefónico,'
                  ' estos deben ir separados por coma (,).',
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message='El dato no es válido, sólo se permiten números.'
                        ' Si desea ingresar más de un número telefónico,'
                        ' estos deben estar separados por coma (,).'
            ),
            MinLengthValidator(6),
        ],
        error_messages={
            'min_length':
                'El campo "Número telefónico" debe tener al menos '
                '%(limit_value)d dígitos (actualmente tiene %(show_value)d).'
        }
    )

    leaseholder_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='correo electrónico del arrendatario',
    )

    observations = models.TextField(
        blank=True,
        verbose_name='observaciones',
    )

    activity_log = models.TextField(
        blank=True,
        verbose_name='registro de actividad',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def get_absolute_url(self):
        return reverse(
            'buildings:unit_detail', args=[self.building.id, self.id]
        )

    def __str__(self):
        if self.block:
            return '{0} - {1}'.format(
                self.block,
                self.unit,
            )

        return self.unit

    class Meta:
        verbose_name = 'unidad'
        verbose_name_plural = 'unidades'
        ordering = ('block', 'unit')
