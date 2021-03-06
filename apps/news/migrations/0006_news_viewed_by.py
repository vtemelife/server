# Generated by Django 2.1.5 on 2019-08-20 10:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("news", "0005_auto_20190820_0950")]

    operations = [
        migrations.AddField(
            model_name="news",
            name="viewed_by",
            field=models.ManyToManyField(
                blank=True, related_name="user_viewed_news", to=settings.AUTH_USER_MODEL, verbose_name="Viewed by"
            ),
        )
    ]
