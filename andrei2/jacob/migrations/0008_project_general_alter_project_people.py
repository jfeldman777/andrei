# Generated by Django 4.2 on 2023-04-26 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jacob', '0007_alter_task_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='general',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='he', to='jacob.userprofile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='people',
            field=models.ManyToManyField(related_name='they', to='jacob.userprofile'),
        ),
    ]