# Generated by Django 2.1.5 on 2019-03-31 23:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shops", "0002_auto_20190331_2300"),
        ("storage", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="administrator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Administrator"
            ),
        ),
        migrations.AddField(
            model_name="shop",
            name="avatar",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="storage.Image",
                verbose_name="Avatar",
            ),
        ),
        migrations.AddField(
            model_name="shop",
            name="moderators",
            field=models.ManyToManyField(
                blank=True, related_name="moderator_shops", to=settings.AUTH_USER_MODEL, verbose_name="Moderators"
            ),
        ),
    ]
