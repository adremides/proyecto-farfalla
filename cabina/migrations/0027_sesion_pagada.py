# Generated by Django 2.1 on 2018-10-09 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0026_auto_20181008_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='pagada',
            field=models.BooleanField(default=False, verbose_name='Pagada'),
        ),
    ]
