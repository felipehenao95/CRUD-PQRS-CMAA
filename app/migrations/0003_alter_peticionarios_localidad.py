# Generated by Django 5.0.4 on 2024-05-20 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_peticionarios_barrio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticionarios',
            name='localidad',
            field=models.CharField(blank=True, choices=[('Usaquén', 'Usaquén'), ('Chapinero', 'Chapinero'), ('Santa Fe', 'Santa Fe'), ('Suba', 'Suba')], max_length=50),
        ),
    ]
