# Generated by Django 4.2 on 2023-05-07 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jacob", "0010_remove_less_end_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="general",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="he",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
