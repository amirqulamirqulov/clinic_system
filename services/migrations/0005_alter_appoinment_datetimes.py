# Generated by Django 5.0.4 on 2024-05-09 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_rename_datetime_appoinment_datetimes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appoinment',
            name='datetimes',
            field=models.DateTimeField(blank=True, null=True, verbose_name='datetimes'),
        ),
    ]
