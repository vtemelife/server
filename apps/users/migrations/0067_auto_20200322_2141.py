# Generated by Django 2.2.10 on 2020-03-22 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0066_auto_20200220_1416")]

    operations = [
        migrations.AlterField(
            model_name="user", name="privacy", field=models.BooleanField(default=False, verbose_name="Privacy")
        )
    ]
