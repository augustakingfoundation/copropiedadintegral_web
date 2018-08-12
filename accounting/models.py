from django.db import models
from django.utils.translation import gettext_lazy as _


class Accounting(models.Model):
    """
    """
    condo = models.OneToOneField(
        'buildings.Building',
        on_delete=models.CASCADE,
        verbose_name=_('unidad'),
    )

    initial_period = models.DateField(
        verbose_name=_('periodo inicial'),
    )

    economic_activity = models.ForeignKey(
        'accounting.EconomicActivity',
        on_delete=models.CASCADE,
        verbose_name=_('actividad económica'),
    )

    apply_retention = models.BooleanField(
        default=False,
        verbose_name=_('aplica retención a título de impuesto de renta'),
    )

    is_self_withholding = models.BooleanField(
        default=False,
        verbose_name=_('es autorretenedor a título impuesto de renta'),
    )

    rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('tarifa'),
    )

    nit_dian = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=_('Nit DIAN'),
    )

    local_nit_dian = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=_('Nit DIAN local'),
        help_text=_('Secretaría de hacienda distrital SHD'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return 'Contabilidad - {0}'.format(
            self.condo,
        )

    class Meta:
        verbose_name = _('contabilidad')
        verbose_name_plural = _('contabilidades')
        ordering = ('condo',)


class EconomicActivity(models.Model):
    code = models.IntegerField(
        verbose_name=_('código'),
    )

    name = models.CharField(
        max_length=200,
        verbose_name=_('nombre'),
    )

    rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_('tarifa'),
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.code,
            self.name,
        )

    class Meta:
        verbose_name = _('actividad económica')
        verbose_name_plural = _('actividades aconómicas')
        ordering = ('code',)
