# Generated by Django 2.1.5 on 2020-02-16 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("events", "0015_auto_20200216_0748")]

    operations = [migrations.RenameField(model_name="party", old_name="title", new_name="name")]
