# Generated by Django 2.1.5 on 2019-05-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("posts", "0011_auto_20190424_2036")]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[
                    ("waiting", "Waiting"),
                    ("waiting_moderation", "Waiting moderation"),
                    ("approved", "Approved"),
                    ("declined", "Declined"),
                ],
                db_index=True,
                default="waiting",
                max_length=32,
                verbose_name="Status",
            ),
        )
    ]
