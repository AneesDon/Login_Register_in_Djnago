# Generated by Django 4.1 on 2024-01-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custombaseuser',
            name='user_type',
        ),
        migrations.AddField(
            model_name='custombaseuser',
            name='is_buyer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='custombaseuser',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]