# Generated by Django 2.1 on 2018-10-26 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0031_auto_20181026_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cabina.Responsable'),
        ),
        migrations.AlterField(
            model_name='sesion',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cabina.Responsable'),
        ),
    ]
