# Generated by Django 2.1.5 on 2019-05-17 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("posts", "0016_auto_20190517_2023")]

    operations = [migrations.RenameField(model_name="post", old_name="hashtags", new_name="hash_tags")]
