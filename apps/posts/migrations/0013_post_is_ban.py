# Generated by Django 2.1.5 on 2019-05-07 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("posts", "0012_auto_20190507_0622")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_ban",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is ban"),
        )
    ]
