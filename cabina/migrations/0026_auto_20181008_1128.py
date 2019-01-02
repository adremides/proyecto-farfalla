# Generated by Django 2.1 on 2018-10-08 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabina', '0025_auto_20180928_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=75)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='consintio',
            field=models.BooleanField(default=False, verbose_name='Consintió'),
        ),
        migrations.AddField(
            model_name='sesion',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cabina.Responsable'),
        ),
    ]