# Generated by Django 2.1.5 on 2019-05-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("games", "0007_remove_gameuser_expired")]

    operations = [
        migrations.AddField(
            model_name="game",
            name="slug",
            field=models.SlugField(default="fancy", max_length=150, unique=True, verbose_name="Slug"),
            preserve_default=False,
        )
    ]
