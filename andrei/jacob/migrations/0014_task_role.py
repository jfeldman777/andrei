# Generated by Django 4.2 on 2023-05-13 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0013_userprofile_res'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jacob.role'),
        ),
    ]
