# Generated by Django 2.1.5 on 2019-09-22 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("news", "0009_auto_20190909_2327")]

    operations = [
        migrations.AddField(
            model_name="news",
            name="slug",
            field=models.SlugField(blank=True, max_length=150, null=True, verbose_name="Slug"),
        )
    ]
