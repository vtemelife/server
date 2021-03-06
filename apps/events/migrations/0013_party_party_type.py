# Generated by Django 2.1.5 on 2019-10-08 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0012_auto_20191007_0911")]

    operations = [
        migrations.AddField(
            model_name="party",
            name="party_type",
            field=models.CharField(
                choices=[("open", "Open"), ("close", "Close")],
                db_index=True,
                default="open",
                max_length=16,
                verbose_name="Type",
            ),
            preserve_default=False,
        )
    ]
