# Generated by Django 2.1.5 on 2019-08-17 11:38

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0043_auto_20190817_1132")]

    operations = [
        migrations.CreateModel(
            name="SocialLink",
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
                ("link", models.URLField(verbose_name="Link")),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_sociallinks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
            ],
            options={"verbose_name": "Socil Link", "verbose_name_plural": "Socil Links"},
        )
    ]
