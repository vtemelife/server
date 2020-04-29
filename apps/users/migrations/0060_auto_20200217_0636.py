# Generated by Django 2.1.5 on 2020-02-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0059_user_privacy")]

    operations = [
        migrations.RenameField(model_name="user", old_name="username", new_name="name"),
        migrations.AlterField(
            model_name="user",
            name="slug",
            field=models.SlugField(max_length=150, unique=True, verbose_name="Username (slug)"),
        ),
    ]
