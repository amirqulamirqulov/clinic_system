# Generated by Django 5.0.4 on 2024-05-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='price'),
        ),
    ]