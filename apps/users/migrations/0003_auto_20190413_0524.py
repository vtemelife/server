# Generated by Django 2.1.5 on 2019-04-13 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0002_auto_20190409_1029")]

    operations = [
        migrations.AlterModelOptions(name="user", options={"verbose_name": "User", "verbose_name_plural": "Users"}),
        migrations.AlterModelOptions(
            name="userfriend", options={"verbose_name": "User friend", "verbose_name_plural": "User friends"}
        ),
    ]
