# Generated by Django 2.1 on 2018-10-29 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0032_auto_20181026_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='pack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cabina.Pack'),
        ),
    ]