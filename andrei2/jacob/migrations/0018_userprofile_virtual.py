# Generated by Django 4.2 on 2023-05-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0017_alter_less_load_alter_task_load'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='virtual',
            field=models.BooleanField(default=False),
        ),
    ]