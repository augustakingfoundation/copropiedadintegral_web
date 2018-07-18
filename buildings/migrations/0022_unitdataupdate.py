# Generated by Django 2.0.5 on 2018-07-18 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0021_auto_20180709_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitDataUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_owners_update', models.BooleanField(default=False, verbose_name='habilitar actualización de propietarios')),
                ('unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='buildings.Unit', verbose_name='unidad')),
            ],
        ),
    ]
