# Generated by Django 5.0.4 on 2024-05-11 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('erkak', 'male'), ('ayol', 'female')], max_length=10, null=True, verbose_name='gender'),
        ),
    ]