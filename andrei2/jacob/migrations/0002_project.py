# Generated by Django 4.2 on 2023-04-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]