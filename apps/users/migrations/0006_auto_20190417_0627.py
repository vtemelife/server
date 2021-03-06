# Generated by Django 2.1.5 on 2019-04-17 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0005_auto_20190415_1943")]

    operations = [
        migrations.RemoveField(model_name="user", name="status"),
        migrations.RemoveField(model_name="userfriend", name="status"),
        migrations.AddField(
            model_name="user",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is deleted"),
        ),
        migrations.AddField(
            model_name="userfriend",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is deleted"),
        ),
    ]
