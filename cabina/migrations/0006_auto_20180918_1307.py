# Generated by Django 2.1 on 2018-09-18 16:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0005_auto_20180918_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jsignaturemodel',
            name='turno',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha_incorporacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 16, 7, 20, 144368, tzinfo=utc), verbose_name='fecha de incorporación'),
        ),
    ]
