# Generated by Django 2.1.5 on 2019-08-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("media", "0020_auto_20190517_2023")]

    operations = [
        migrations.RemoveField(model_name="hotdaiting", name="creator"),
        migrations.RemoveField(model_name="hotdaiting", name="image"),
        migrations.AddField(
            model_name="media",
            name="hot_daiting_status",
            field=models.CharField(
                blank=True,
                choices=[("waiting", "Waiting moderation"), ("approved", "Approved"), ("declined", "Declined")],
                db_index=True,
                max_length=32,
                null=True,
                verbose_name="Hot daiting status",
            ),
        ),
        migrations.DeleteModel(name="HotDaiting"),
    ]
