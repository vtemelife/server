# Generated by Django 2.1.5 on 2020-02-16 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("chat", "0026_auto_20190923_1938")]

    operations = [
        migrations.RemoveField(model_name="chat", name="content_type"),
        migrations.RemoveField(model_name="chat", name="object_id"),
    ]
