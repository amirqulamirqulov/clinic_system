# Generated by Django 5.0.4 on 2024-05-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_date_of_birth_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='price',
            field=models.IntegerField(blank=True, max_length=50, null=True, verbose_name='price'),
        ),
    ]
