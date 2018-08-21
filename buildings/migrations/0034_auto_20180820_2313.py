# Generated by Django 2.0.5 on 2018-08-21 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0033_unitdataupdate_domestic_workers_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitdataupdate',
            name='pets_update',
            field=models.BooleanField(default=False, verbose_name='edición de mascotas habilitada'),
        ),
        migrations.AlterField(
            model_name='unitdataupdate',
            name='domestic_workers_update',
            field=models.BooleanField(default=False, verbose_name='edición de trabajadores domésticos habilitada'),
        ),
        migrations.AlterField(
            model_name='unitdataupdate',
            name='residents_update',
            field=models.BooleanField(default=False, verbose_name='edición de residentes habilitada'),
        ),
        migrations.AlterField(
            model_name='unitdataupdate',
            name='vehicles_update',
            field=models.BooleanField(default=False, verbose_name='edición de vehículos habilitada'),
        ),
        migrations.AlterField(
            model_name='unitdataupdate',
            name='visitors_update',
            field=models.BooleanField(default=False, verbose_name='edición de visitantes habilitada'),
        ),
    ]