# Generated by Django 2.1.5 on 2019-04-16 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0003_auto_20190413_0524")]

    operations = [migrations.RenameField(model_name="event", old_name="administrator", new_name="creator")]
