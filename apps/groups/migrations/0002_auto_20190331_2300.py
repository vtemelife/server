# Generated by Django 2.1.5 on 2019-03-31 23:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("storage", "0001_initial"),
        ("groups", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="administrator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Administrator"
            ),
        ),
        migrations.AddField(
            model_name="group",
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
            model_name="group",
            name="moderators",
            field=models.ManyToManyField(
                blank=True, related_name="moderator_groups", to=settings.AUTH_USER_MODEL, verbose_name="Moderators"
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="user_groups", to=settings.AUTH_USER_MODEL, verbose_name="Users"
            ),
        ),
    ]
