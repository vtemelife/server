# Generated by Django 2.1.5 on 2019-04-09 10:29

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="userfriend", options={"verbose_name": "user friend", "verbose_name_plural": "user friends"}
        ),
        migrations.AlterField(
            model_name="user",
            name="relationship_themes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[("swing", "Swing"), ("bdsm", "Bdsm"), ("virt", "Virt"), ("other", "Other")], max_length=16
                ),
                null=True,
                size=None,
                verbose_name="Relationship themes",
            ),
        ),
        migrations.AlterField(
            model_name="userfriend",
            name="friend",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friend_users",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Content type",
            ),
        ),
    ]
