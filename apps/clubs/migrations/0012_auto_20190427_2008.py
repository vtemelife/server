# Generated by Django 2.1.5 on 2019-04-27 20:08

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("clubs", "0011_auto_20190423_1432")]

    operations = [
        migrations.CreateModel(
            name="ClubRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="uuid", default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True, verbose_name="Created date")),
                ("updated_date", models.DateTimeField(auto_now=True, verbose_name="Updated date")),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="club_club_requests",
                        to="clubs.Club",
                        verbose_name="Club",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_club_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={"verbose_name": "User request", "verbose_name_plural": "User requests"},
        ),
        migrations.AlterUniqueTogether(name="clubrequest", unique_together={("user", "club")}),
    ]
