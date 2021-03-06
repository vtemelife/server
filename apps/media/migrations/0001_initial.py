# Generated by Django 2.1.5 on 2019-03-31 23:00

import uuid

import apps.media.models
import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("contenttypes", "0002_remove_content_type_name")]

    operations = [
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="uuid", default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("deleted", "Deleted"), ("created", "Created"), ("approved", "Approved")],
                        default="created",
                        max_length=32,
                        verbose_name="Status",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True, verbose_name="Created date")),
                ("updated_date", models.DateTimeField(auto_now=True, verbose_name="Updated date")),
                ("object_id", models.UUIDField(verbose_name="Object UUID")),
                ("title", models.CharField(blank=True, max_length=255, null=True, verbose_name="Title")),
                ("description", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Description")),
                (
                    "video_code",
                    models.CharField(blank=True, max_length=255, null=True, verbose_name="Embed video code"),
                ),
                ("hash_tags", models.TextField(blank=True, null=True, verbose_name="Hash tags")),
                ("likes", models.PositiveIntegerField(default=0, verbose_name="Likes")),
                ("views", models.PositiveIntegerField(default=0, verbose_name="Views")),
                (
                    "media_type",
                    models.CharField(
                        choices=[("photo", "Photo"), ("video", "Video")], max_length=16, verbose_name="Type"
                    ),
                ),
                ("published_for_all", models.BooleanField(default=False, verbose_name="Published for All")),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to=apps.media.models.limit_choices_to_content_type,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                        verbose_name="Content type",
                    ),
                ),
            ],
            options={"verbose_name": "media", "verbose_name_plural": "media"},
        )
    ]
