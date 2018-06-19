from django.db import models

from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('departamento'),
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.name,
            self.state,
        )

    class Meta:
        ordering = ('name',)
        verbose_name = _('ciudad')
        verbose_name_plural = _('ciudades')


class State(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('nombre'),
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _('departamento')
        verbose_name_plural = _('departamentos')
