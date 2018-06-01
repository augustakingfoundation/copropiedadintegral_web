from django.db import models


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='nombre',
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='departamento',
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = 'ciudad'
        verbose_name_plural = 'ciudades'


class State(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='nombre',
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
