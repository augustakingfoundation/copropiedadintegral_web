# Generated by Django 2.0.5 on 2018-07-31 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0027_owner_is_resident'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitdataupdate',
            name='enable_leaseholders_update',
            field=models.BooleanField(default=False, verbose_name='habilitar actualización de arrendatarios'),
        ),
        migrations.AddField(
            model_name='unitdataupdate',
            name='leaseholders_update_key',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='clave actualizar residentes'),
        ),
    ]
