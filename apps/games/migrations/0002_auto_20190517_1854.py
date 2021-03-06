# Generated by Django 2.1.5 on 2019-05-17 18:54

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0003_auto_20190417_0627"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameUser",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="uuid", default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True, verbose_name="Created date")),
                ("updated_date", models.DateTimeField(auto_now=True, verbose_name="Updated date")),
                ("is_deleted", models.BooleanField(db_index=True, default=False, verbose_name="Is deleted")),
                (
                    "game_data",
                    django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name="Game data"),
                ),
            ],
            options={"verbose_name": "Game User", "verbose_name_plural": "Game Users"},
        ),
        migrations.AddField(
            model_name="game",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="storage.Image",
                verbose_name="Image",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="is_ban",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is ban"),
        ),
        migrations.AddField(
            model_name="game",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("waiting", "Waiting moderation"), ("approved", "Approved"), ("declined", "Declined")],
                db_index=True,
                max_length=32,
                null=True,
                verbose_name="Status",
            ),
        ),
        migrations.AddField(
            model_name="game", name="token", field=models.UUIDField(blank=True, null=True, verbose_name="Token")
        ),
        migrations.AddField(
            model_name="gameuser",
            name="game",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="games.Game", verbose_name="Game"),
        ),
        migrations.AddField(
            model_name="gameuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="User"
            ),
        ),
    ]
