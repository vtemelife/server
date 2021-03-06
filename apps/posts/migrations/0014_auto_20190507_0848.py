# Generated by Django 2.1.5 on 2019-05-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("posts", "0013_post_is_ban")]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("waiting", "Waiting moderation"), ("approved", "Approved"), ("declined", "Declined")],
                db_index=True,
                max_length=32,
                null=True,
                verbose_name="Status",
            ),
        )
    ]
