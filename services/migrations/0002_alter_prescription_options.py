# Generated by Django 5.0.4 on 2024-05-03 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prescription',
            options={'verbose_name': 'prescription', 'verbose_name_plural': 'prescriptions'},
        ),
    ]
