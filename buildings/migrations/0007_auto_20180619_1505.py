# Generated by Django 2.0.5 on 2018-06-19 20:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0006_auto_20180618_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='phone_number',
            field=models.CharField(blank=True, error_messages={'min_length': 'El campo "Número telefónico" debe tener al menos %(limit_value)d dígitos (actualmente tiene %(show_value)d).'}, help_text='Si desea ingresar más de un número telefónico,estos deben ir separados por coma (,).', max_length=32, validators=[django.core.validators.RegexValidator('^[0-9 ,]*$', message='El dato no es válido, sólo debe ingresar números. Si desea ingresar más de un número celular, estos deben estar separados por coma (,).'), django.core.validators.MinLengthValidator(6)], verbose_name='número telefónico'),
        ),
        migrations.AlterField(
            model_name='leaseholder',
            name='phone_number',
            field=models.CharField(blank=True, error_messages={'min_length': 'El campo "Número telefónico" debe tener al menos %(limit_value)d dígitos (actualmente tiene %(show_value)d).'}, help_text='Si desea ingresar más de un número telefónico,estos deben ir separados por coma (,).', max_length=32, validators=[django.core.validators.RegexValidator('^[0-9 ,]*$', message='El dato no es válido, sólo debe ingresar números. Si desea ingresar más de un número celular, estos deben estar separados por coma (,).'), django.core.validators.MinLengthValidator(6)], verbose_name='número telefónico'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='phone_number',
            field=models.CharField(blank=True, error_messages={'min_length': 'El campo "Número telefónico" debe tener al menos %(limit_value)d dígitos (actualmente tiene %(show_value)d).'}, help_text='Si desea ingresar más de un número telefónico, estos deben ir separados por coma (,).', max_length=32, validators=[django.core.validators.RegexValidator('^[0-9 ,]*$', message='El dato no es válido, sólo debe ingresar números. Si desea ingresar más de un número celular, estos deben estar separados por coma (,).'), django.core.validators.MinLengthValidator(6)], verbose_name='número telefónico'),
        ),
    ]