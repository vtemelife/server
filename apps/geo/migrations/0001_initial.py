# Generated by Django 2.1.5 on 2019-05-04 09:49

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
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
                ("name_ru", models.CharField(db_index=True, max_length=255, verbose_name="Name(ru)")),
                ("name_en", models.CharField(db_index=True, max_length=255, verbose_name="Name(en)")),
                ("latitude", models.FloatField(blank=True, null=True, verbose_name="Latitude")),
                ("longitude", models.FloatField(blank=True, null=True, verbose_name="Longitude")),
                ("city_id", models.IntegerField(blank=True, null=True)),
            ],
            options={"verbose_name": "City", "verbose_name_plural": "Cities"},
        ),
        migrations.CreateModel(
            name="Country",
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
                ("code", models.CharField(db_index=True, max_length=3, null=True, unique=True, verbose_name="Code")),
                ("name_ru", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="Name(ru)")),
                ("name_en", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="Name(en)")),
                ("country_id", models.IntegerField(blank=True, null=True)),
            ],
            options={"verbose_name": "Country", "verbose_name_plural": "Countries"},
        ),
        migrations.CreateModel(
            name="Region",
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
                ("name_ru", models.CharField(db_index=True, max_length=255, verbose_name="Name(ru)")),
                ("name_en", models.CharField(db_index=True, max_length=255, verbose_name="Name(en)")),
                ("region_id", models.IntegerField(blank=True, null=True)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="country_regions",
                        to="geo.Country",
                        verbose_name="Country",
                    ),
                ),
            ],
            options={"verbose_name": "Region", "verbose_name_plural": "Regions"},
        ),
        migrations.AddField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="country_cities",
                to="geo.Country",
                verbose_name="Country",
            ),
        ),
        migrations.AddField(
            model_name="city",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="region_cities",
                to="geo.Region",
                verbose_name="Region",
            ),
        ),
        migrations.AlterUniqueTogether(name="region", unique_together={("country", "name_en"), ("country", "name_ru")}),
        migrations.AlterUniqueTogether(
            name="city", unique_together={("country", "region", "name_ru"), ("country", "region", "name_en")}
        ),
    ]
