# Generated by Django 4.2 on 2023-05-08 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0012_userprofile_fio'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='res',
            field=models.ManyToManyField(default=None, related_name='they', to='jacob.role'),
        ),
    ]
