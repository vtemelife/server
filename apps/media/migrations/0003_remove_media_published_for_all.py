# Generated by Django 2.1.5 on 2019-03-31 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("media", "0002_auto_20190331_2300")]

    operations = [migrations.RemoveField(model_name="media", name="published_for_all")]
