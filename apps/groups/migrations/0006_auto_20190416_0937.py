# Generated by Django 2.1.5 on 2019-04-16 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("groups", "0005_auto_20190416_0937")]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Creator"
            ),
        )
    ]
