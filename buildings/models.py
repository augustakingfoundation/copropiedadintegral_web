from hashids import Hashids

from datetime import date
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .data import BUILDING_DOCUMENT_TYPE_CHOICES
from .data import PARKING_LOT_TYPE_CHOICES
from .data import VEHICLE_TYPE_BICYCLE
from .data import VEHICLE_TYPE_CAR
from .data import VEHICLE_TYPE_CHOICES
from .data import VEHICLE_TYPE_MOTORCYCLE
from .data import MEMBERSHIP_TYPE_CHOICES
from .data import MEMBERSHIP_TYPE_ADMINISTRATOR
from .data import MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT
from .data import MEMBERSHIP_TYPE_ACCOUNTANT
from .data import MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT
from .data import MEMBERSHIP_TYPE_FISCAL_REVIEWER
from accounts.data import DOCUMENT_TYPE_CHOICES
from app.validators import FileSizeValidator


class BuildingMembership(models.Model):
    """
    This model represents a membership of user in
    a building or condo. Memberships can have
    different roles: Administrator, administrative assistant,
    accountant, accounting assistant and fiscal reviewer.
    """
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_('usuario'),
    )

    building = models.ForeignKey(
        'buildings.Building',
        on_delete=models.CASCADE,
        verbose_name=_('copropiedad'),
    )

    membership_type = models.PositiveSmallIntegerField(
        choices=MEMBERSHIP_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    is_active = models.BooleanField(
        verbose_name=_('membresía activa'),
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def is_main_administrator(self):
        if (
            self.building.created_by == self.user and
            self.membership_type == MEMBERSHIP_TYPE_ADMINISTRATOR
        ):
            return True
        return False

    @property
    def is_administrator(self):
        if (
            self.membership_type == MEMBERSHIP_TYPE_ADMINISTRATOR and
            not self.building.created_by == self.user
        ):
            return True
        return False

    @property
    def is_administrative_assistant(self):
        return self.membership_type == MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT

    @property
    def is_accountant(self):
        return self.membership_type == MEMBERSHIP_TYPE_ACCOUNTANT

    @property
    def is_accounting_assistant(self):
        return self.membership_type == MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT

    @property
    def is_fiscal_reviewer(self):
        return self.membership_type == MEMBERSHIP_TYPE_FISCAL_REVIEWER

    def __str__(self):
        return '{0}'.format(self.user)

    class Meta:
        verbose_name = _('membresía')
        verbose_name_plural = _('membresías')
        ordering = ('created_at',)
        unique_together = (
            ('user', 'building'),
        )


class Building(models.Model):
    """
    This model represents a building, condo or coproperty.
    a condo is a type of real estate divided into several
    units that are each separately owned, surrounded by
    common areas jointly owned.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=BUILDING_DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=_('documento/Nit'),
    )

    logo = models.ImageField(
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    city = models.ForeignKey(
        'place.City',
        verbose_name=_('ciudad'),
        on_delete=models.DO_NOTHING,
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('dirección'),
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('correo electrónico'),
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name=_('número celular'),
        default='',
        blank=True,
        help_text=_('Si desea ingresar más de un número celular, '
                    'estos deben ir separados por coma (,).'
                    ),
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
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
        verbose_name=_('número telefónico'),
        help_text=_('Si desea ingresar más de un número telefónico,'
                    'estos deben ir separados por coma (,).'
                    ),
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
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
        verbose_name=_('periodo inicial'),
    )

    activity_log = models.TextField(
        blank=True,
        verbose_name=_('registro de actividad'),
    )

    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_('creado por'),
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
        verbose_name = _('copropiedad')
        verbose_name_plural = _('copropiedades')
        ordering = ('created_at',)


class Unit(models.Model):
    """
    This model represents an apartment, house or office
    that is part of a condo.
    """
    building = models.ForeignKey(
        'buildings.Building',
        on_delete=models.CASCADE,
        verbose_name=_('copropiedad'),
    )

    block = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('bloque'),
        help_text=_('Bloque o interior'),
    )

    unit = models.CharField(
        max_length=50,
        verbose_name='unidad',
        help_text=_('Apartamento, casa u oficina'),
    )

    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('área (Mts)'),
    )

    real_estate_registration = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('matrícula inmobiliaria'),
    )

    coefficient = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        blank=True,
        verbose_name=_('Coeficiente'),
        help_text=_('Este valor debe ser un porcentaje entre 0 y 100'),
    )

    observations = models.TextField(
        blank=True,
        verbose_name=_('observaciones'),
    )

    activity_log = models.TextField(
        blank=True,
        verbose_name=_('registro de actividad'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def owner_has_email(self):
        has_email = False
        for owner in self.owner_set.all():
            if owner.email:
                has_email = True

        return has_email

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
        verbose_name = _('unidad')
        verbose_name_plural = _('unidades')
        ordering = ('block', 'unit')


class UnitDataUpdate(models.Model):
    """
    This model is used to manage permissions on data
    update functionalities per each registered unit.
    """
    unit = models.OneToOneField(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    enable_owners_update = models.BooleanField(
        verbose_name=_('habilitar actualización de propietarios'),
        default=False,
    )

    owners_update_key = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('clave actualizar propietarios'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def owners_data_key(self):
        hashids = Hashids(salt=self.owners_update_key, min_length=50)
        return hashids.encode(self.id)

    def __str__(self):
        if self.unit.block:
            return 'Bloque {0} - Unidad {1}'.format(
                self.unit.block,
                self.unit.unit,
            )

        return '{0}'.format(self.unit)

    class Meta:
        verbose_name = _('Información de actualización unidad')
        verbose_name_plural = _('Información de actualización unidades')
        ordering = ('unit',)


class Owner(models.Model):
    """
    This model represents a unit owner. At least one
    owner is required by each unit. Multiple owners
    can be added to a unit.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        verbose_name=_('número de documento'),
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name=_('número celular'),
        default='',
        blank=True,
        help_text=_('Si desea ingresar más de un número celular, '
                    'estos deben ir separados por coma (,).'
                    ),
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
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
        verbose_name=_('número telefónico'),
        help_text=_('Si desea ingresar más de un número telefónico, '
                    'estos deben ir separados por coma (,).'),
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
            ),
            MinLengthValidator(6),
        ],
        error_messages={
            'min_length':
                'El campo "Número telefónico" debe tener al menos '
                '%(limit_value)d dígitos (actualmente tiene %(show_value)d).'
        }
    )

    correspondence_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('dirección de correspondencia'),
        help_text=_('Dirección alternativa para enviar correspondencia '
                    'al propietario de la unidad'),
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('correo electrónico'),
    )

    is_main = models.BooleanField(
        verbose_name=_('propietario principal'),
        default=False,
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def __str__(self):
        return '{0} {1} - {2}'.format(
            self.name,
            self.last_name,
            self.unit,
        )

    class Meta:
        verbose_name = _('propietario')
        verbose_name_plural = _('propietarios')
        ordering = ('last_name',)


class Leaseholder(models.Model):
    """
    This model represents a unit leaseholder. Leaseholders
    are not required.  Multiple leaseholders can be added to
    a unit.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        verbose_name=_('número de documento'),
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name=_('número celular'),
        default='',
        blank=True,
        help_text=_('Si desea ingresar más de un número celular, '
                    'estos deben ir separados por coma (,).'),
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
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
        verbose_name=_('número telefónico'),
        help_text=_('Si desea ingresar más de un número telefónico,'
                    'estos deben ir separados por coma (,).'),
        blank=True,
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
            ),
            MinLengthValidator(6),
        ],
        error_messages={
            'min_length':
                'El campo "Número telefónico" debe tener al menos '
                '%(limit_value)d dígitos (actualmente tiene %(show_value)d).'
        }
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('correo electrónico'),
    )

    is_main = models.BooleanField(
        verbose_name=_('arrendatario principal'),
        default=False,
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def __str__(self):
        return '{0} {1} - {2}'.format(
            self.name,
            self.last_name,
            self.unit,
        )

    class Meta:
        verbose_name = _('arrendatario')
        verbose_name_plural = _('arrendatarios')
        ordering = ('last_name',)


class EmergencyContact(models.Model):
    """
    This model represent an emergency contact of
    a resident.
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name=_('número celular'),
        help_text=_('Si desea ingresar más de un número celular, '
                    'estos deben ir separados por coma (,).'),
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
            ),
            MinLengthValidator(10),
        ],
        error_messages={
            'min_length':
                'Ingrese al menos %(limit_value)d caracteres,'
                ' (actualmente tiene %(show_value)d).'
        }
    )

    resident = models.ForeignKey(
        'buildings.Resident',
        on_delete=models.CASCADE,
        verbose_name=_('residente'),
    )

    def __str__(self):
        return '{0} {1}'.format(
            self.first_name,
            self.last_name,
        )

    class Meta:
        verbose_name = _('contacto de emergencia')
        verbose_name_plural = _('contactos de emergencia')
        ordering = ('last_name',)


class Resident(models.Model):
    """
    This model represents a resident
    registered in a unit.
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    birthdate = models.DateField(
        verbose_name=_('fecha de nacimiento'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        verbose_name=_('número de documento'),
    )

    mobile_phone = models.CharField(
        max_length=32,
        verbose_name=_('número celular'),
        default='',
        blank=True,
        help_text=_('Si desea ingresar más de un número celular, '
                    'estos deben ir separados por coma (,).'),
        validators=[
            RegexValidator(
                '^[0-9 ,]*$',
                message=_('El dato no es válido, sólo debe ingresar números. '
                          'Si desea ingresar más de un número celular, estos '
                          'deben estar separados por coma (,).')
            ),
            MinLengthValidator(10),
        ],
        error_messages={
            'min_length':
                'Ingrese al menos %(limit_value)d caracteres,'
                ' (actualmente tiene %(show_value)d).'
        }
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def get_absolute_url(self):
        return reverse(
            'buildings:resident_detail',
            args=[self.unit.building.id, self.unit.id, self.id]
        )

    @property
    def calculate_age(self):
        today = date.today()
        if self.birthdate:
            try:
                birthday = self.birthdate.replace(year=today.year)
            except ValueError:
                birthday = self.birthdate.replace(
                    year=today.year, day=self.birthdate.day - 1
                )
            if birthday > today:
                return today.year - self.birthdate.year - 1
            else:
                return today.year - self.birthdate.year

        return 0

    def __str__(self):
        return '{0} {1} | {2} - {3}'.format(
            self.first_name,
            self.last_name,
            self.get_document_type_display(),
            self.document_number,
        )

    class Meta:
        verbose_name = _('residente')
        verbose_name_plural = _('residentes')
        ordering = ('last_name',)


class ParkingLot(models.Model):
    """
    This model represents a parking lot assigned to an
    unit.
    """
    number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('número'),
    )

    parking_lot_type = models.PositiveSmallIntegerField(
        choices=PARKING_LOT_TYPE_CHOICES,
        verbose_name=_('tipo de parqueadero'),
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.unit,
            self.number,
        )

    class Meta:
        verbose_name = _('parqueadero')
        verbose_name_plural = _('parqueaderos')
        ordering = ('number',)


class Vehicle(models.Model):
    """
    This model represents a vehicle assigned to an
    unit.
    """
    brand = models.CharField(
        max_length=50,
        verbose_name=_('marca'),
    )

    vehicle_type = models.PositiveSmallIntegerField(
        choices=VEHICLE_TYPE_CHOICES,
        verbose_name=_('tipo de vehículo'),
    )

    license_plate = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('placa'),
    )

    color = models.CharField(
        max_length=50,
        verbose_name=_('color'),
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    @property
    def is_car(self):
        return self.vehicle_type == VEHICLE_TYPE_CAR

    @property
    def is_motorcycle(self):
        return self.vehicle_type == VEHICLE_TYPE_MOTORCYCLE

    @property
    def is_bicycle(self):
        return self.vehicle_type == VEHICLE_TYPE_BICYCLE

    def __str__(self):
        return '{0} - {1}'.format(
            self.unit,
            self.brand,
        )

    class Meta:
        verbose_name = _('vehículo')
        verbose_name_plural = _('vehículos')
        ordering = ('vehicle_type',)


class DomesticWorker(models.Model):
    """
    This model represents a domestic worker registered in
    a unit.
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        verbose_name=_('número de documento'),
    )

    schedule = models.TextField(
        verbose_name=_('horario'),
        help_text=_('Días y horarios en los que va a trabajar.'),
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def __str__(self):
        return '{0} {1} - {2}'.format(
            self.first_name,
            self.last_name,
            self.unit,
        )

    class Meta:
        verbose_name = _('trabajador doméstico')
        verbose_name_plural = _('trabajadores domésticos')
        ordering = ('last_name',)


class Pet(models.Model):
    """
    This model represents a pet registered in
    a unit.
    """
    pet_type = models.CharField(
        max_length=30,
        verbose_name=_('tipo de mascota'),
        help_text=_('perro, gato, etc.'),
    )

    breed = models.CharField(
        max_length=30,
        verbose_name=_('raza'),
    )

    name = models.CharField(
        max_length=30,
        verbose_name=_('nombre'),
    )

    color = models.CharField(
        max_length=50,
        verbose_name=_('color'),
    )

    picture = models.ImageField(
        max_length=255,
        blank=True,
        help_text='150x150',
        validators=[FileSizeValidator(4000)],
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def get_absolute_url(self):
        return reverse(
            'buildings:pet_detail',
            args=[self.unit.building.id, self.unit.id, self.id]
        )

    def __str__(self):
        return '{0} | {1} - {2}'.format(
            self.unit,
            self.pet_type,
            self.name,
        )

    class Meta:
        verbose_name = _('mascota')
        verbose_name_plural = _('mascotas')
        ordering = ('name',)


class Visitor(models.Model):
    """
    This model represents an authorized visitor
    registered in a unit.
    """
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('apellidos'),
    )

    document_type = models.PositiveSmallIntegerField(
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('tipo de documento'),
    )

    document_number = models.CharField(
        max_length=32,
        verbose_name=_('número de documento'),
    )

    relationship = models.CharField(
        max_length=50,
        verbose_name=_('parentesco'),
        help_text=_('Amigo, familiar, etc'),
    )

    unit = models.ForeignKey(
        'buildings.Unit',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    def __str__(self):
        return '{0} {1} | {2} - {3}'.format(
            self.first_name,
            self.last_name,
            self.get_document_type_display(),
            self.document_number,
        )

    class Meta:
        verbose_name = _('visitante autorizado')
        verbose_name_plural = _('visitantes autorizados')
        ordering = ('last_name',)
