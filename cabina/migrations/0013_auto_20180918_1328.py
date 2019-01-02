# Generated by Django 2.1 on 2018-09-18 16:28

from django.db import migrations, models
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0012_auto_20180918_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='prueba',
            name='signature',
            field=jsignature.fields.JSignatureField(blank=True, null=True, verbose_name='Signature'),
        ),
        migrations.AddField(
            model_name='prueba',
            name='signature_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Signature date'),
        ),
    ]
