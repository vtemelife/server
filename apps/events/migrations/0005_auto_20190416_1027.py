# Generated by Django 2.1.5 on 2019-04-16 10:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0004_auto_20190416_1027")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Creator"
            ),
        )
    ]
