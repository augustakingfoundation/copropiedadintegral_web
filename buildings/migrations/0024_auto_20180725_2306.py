# Generated by Django 2.0.5 on 2018-07-26 04:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0023_auto_20180718_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unitdataupdate',
            options={'ordering': ('unit',), 'verbose_name': 'Información de actualización unidad', 'verbose_name_plural': 'Información de actualización unidades'},
        ),
        migrations.AddField(
            model_name='unitdataupdate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]