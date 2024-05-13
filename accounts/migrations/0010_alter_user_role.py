# Generated by Django 5.0.4 on 2024-05-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('shifokor', 'doctor'), ('bemor', 'patient'), ('admin', 'admin')], default='patient', max_length=10, verbose_name='role'),
        ),
    ]