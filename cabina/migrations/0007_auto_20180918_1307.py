# Generated by Django 2.1 on 2018-09-18 16:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0006_auto_20180918_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha_incorporacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 16, 7, 24, 78540, tzinfo=utc), verbose_name='fecha de incorporación'),
        ),
    ]
