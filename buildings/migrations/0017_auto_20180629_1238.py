# Generated by Django 2.0.5 on 2018-06-29 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0016_auto_20180628_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='apellidos')),
                ('document_type', models.PositiveSmallIntegerField(choices=[(100, 'C.C.'), (110, 'C.E.'), (120, 'Pasaporte'), (130, 'Tarjeta de identidad')], verbose_name='tipo de documento')),
                ('document_number', models.CharField(max_length=32, verbose_name='número de documento')),
                ('relationship', models.CharField(max_length=50, verbose_name='parentesco')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Unit', verbose_name='unidad')),
            ],
            options={
                'verbose_name': 'visitante autorizado',
                'verbose_name_plural': 'visitantes autorizados',
                'ordering': ('last_name',),
            },
        ),
        migrations.AlterModelOptions(
            name='domesticworker',
            options={'ordering': ('last_name',), 'verbose_name': 'trabajador doméstico', 'verbose_name_plural': 'trabajadores domésticos'},
        ),
        migrations.AlterModelOptions(
            name='pet',
            options={'ordering': ('name',), 'verbose_name': 'mascota', 'verbose_name_plural': 'mascotas'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ('vehicle_type',), 'verbose_name': 'vehículo', 'verbose_name_plural': 'vehículos'},
        ),
        migrations.AlterField(
            model_name='domesticworker',
            name='document_type',
            field=models.PositiveSmallIntegerField(choices=[(100, 'C.C.'), (110, 'C.E.'), (120, 'Pasaporte'), (130, 'Tarjeta de identidad')], verbose_name='tipo de documento'),
        ),
        migrations.AlterField(
            model_name='leaseholder',
            name='document_type',
            field=models.PositiveSmallIntegerField(choices=[(100, 'C.C.'), (110, 'C.E.'), (120, 'Pasaporte'), (130, 'Tarjeta de identidad')], verbose_name='tipo de documento'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='document_type',
            field=models.PositiveSmallIntegerField(choices=[(100, 'C.C.'), (110, 'C.E.'), (120, 'Pasaporte'), (130, 'Tarjeta de identidad')], verbose_name='tipo de documento'),
        ),
    ]
