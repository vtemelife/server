# Generated by Django 2.1.5 on 2019-03-31 23:00

import uuid

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Shop",
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
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Name")),
                ("description", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Description")),
                ("raiting", models.PositiveIntegerField(default=0, verbose_name="Raiting")),
            ],
            options={"verbose_name": "shop", "verbose_name_plural": "shops"},
        ),
        migrations.CreateModel(
            name="ShopItem",
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
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Name")),
                ("description", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Description")),
                ("price", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Price")),
            ],
            options={"verbose_name": "item", "verbose_name_plural": "items"},
        ),
    ]
