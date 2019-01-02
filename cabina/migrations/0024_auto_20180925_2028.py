# Generated by Django 2.1 on 2018-09-25 23:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0023_auto_20180921_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='duracion',
            field=models.CharField(choices=[('5', '5 minutos'), ('10', '10 minutos')], default=5, max_length=3, verbose_name='Duración'),
        ),
        migrations.AlterField(
            model_name='sesion',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='fecha del turno'),
        ),
    ]
