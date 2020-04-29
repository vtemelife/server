# Generated by Django 2.1.5 on 2020-02-16 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("clubs", "0038_auto_20200216_0804")]

    operations = [
        migrations.AddField(
            model_name="club",
            name="slug",
            field=models.SlugField(max_length=150, null=True, unique=True, verbose_name="Slug"),
        ),
        migrations.AlterField(
            model_name="club",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="storage.Image",
                verbose_name="Image",
            ),
        ),
    ]
