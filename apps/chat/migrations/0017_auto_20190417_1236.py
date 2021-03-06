# Generated by Django 2.1.5 on 2019-04-17 12:36

import apps.chat.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chat", "0016_auto_20190417_1222")]

    operations = [
        migrations.RemoveField(model_name="message", name="chat"),
        migrations.AlterField(
            model_name="message",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="contenttypes.ContentType", verbose_name="Content type"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="message",
            name="object_id",
            field=models.UUIDField(verbose_name="Object UUID"),
            preserve_default=False,
        ),
    ]
