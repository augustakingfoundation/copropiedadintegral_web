# Generated by Django 2.0.5 on 2018-07-26 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0024_auto_20180725_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitdataupdate',
            name='owners_update_key',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='clave actualizar propietarios'),
        ),
    ]
