# Generated by Django 2.1.5 on 2020-02-16 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0018_auto_20200216_0756")]

    operations = [
        migrations.AlterField(
            model_name="party",
            name="club",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clubs.Club", verbose_name="Club"),
        )
    ]
