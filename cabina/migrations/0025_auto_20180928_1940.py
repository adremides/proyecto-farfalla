# Generated by Django 2.1 on 2018-09-28 22:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0024_auto_20180925_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='fecha de la sesión'),
        ),
    ]