# Generated by Django 2.1.5 on 2019-08-17 11:32

import apps.users.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0042_user_black_list")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birthday_m",
            field=models.IntegerField(null=True, verbose_name="Birthday (year) man"),
        ),
        migrations.AddField(
            model_name="user",
            name="birthday_w",
            field=models.IntegerField(null=True, verbose_name="Birthday (year) woman"),
        ),
    ]
