# Generated by Django 2.0.5 on 2018-05-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_email',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
