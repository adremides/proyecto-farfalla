# Generated by Django 2.1 on 2018-09-18 16:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0009_auto_20180918_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha_incorporacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 16, 15, 26, 85715, tzinfo=utc), verbose_name='fecha de incorporación'),
        ),
    ]