# Generated by Django 2.1 on 2018-09-18 16:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0004_auto_20180918_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prueba',
            name='cliente',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha_incorporacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 16, 4, 39, 690941, tzinfo=utc), verbose_name='fecha de incorporación'),
        ),
        migrations.DeleteModel(
            name='Prueba',
        ),
    ]
