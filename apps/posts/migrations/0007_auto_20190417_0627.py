# Generated by Django 2.1.5 on 2019-04-17 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("posts", "0006_auto_20190414_1804")]

    operations = [
        migrations.RemoveField(model_name="post", name="status"),
        migrations.AddField(
            model_name="post",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is deleted"),
        ),
    ]
