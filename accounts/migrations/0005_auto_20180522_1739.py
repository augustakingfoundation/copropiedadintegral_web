# Generated by Django 2.0.5 on 2018-05-22 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180522_0148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile_phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]
