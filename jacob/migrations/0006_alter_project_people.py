# Generated by Django 4.2 on 2023-04-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jacob", "0005_project_people"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="people",
            field=models.ManyToManyField(to="jacob.userprofile"),
        ),
    ]
