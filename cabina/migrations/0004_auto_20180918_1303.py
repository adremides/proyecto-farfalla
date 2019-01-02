# Generated by Django 2.1 on 2018-09-18 16:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0003_auto_20180918_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prueba',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='prueba',
            name='signature_date',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha_incorporacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 16, 3, 34, 182206, tzinfo=utc), verbose_name='fecha de incorporación'),
        ),
    ]
