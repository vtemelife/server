# Generated by Django 2.1.5 on 2019-04-16 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("clubs", "0004_auto_20190413_0524")]

    operations = [migrations.RenameField(model_name="club", old_name="administrator", new_name="creator")]
