# Generated by Django 2.0.5 on 2018-06-29 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0015_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domesticworker',
            name='schedule',
            field=models.TextField(help_text='Días y horarios en los que va a trabajar.', verbose_name='horario'),
        ),
    ]
