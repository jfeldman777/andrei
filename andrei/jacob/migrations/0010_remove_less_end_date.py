# Generated by Django 4.2 on 2023-05-05 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0009_less'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='less',
            name='end_date',
        ),
    ]