# Generated by Django 4.2 on 2023-06-07 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jacob", "0019_alter_userprofile_res_alter_userprofile_role_wish"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mygrade",
                    models.CharField(
                        choices=[("0", "-"), ("1", "Jr"), ("2", "Md"), ("3", "Sr")],
                        default="0",
                        max_length=2,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jacob.userprofile",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jacob.role"
                    ),
                ),
            ],
        ),
    ]