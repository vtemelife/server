# Generated by Django 2.1.5 on 2019-08-19 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0048_auto_20190817_1301")]

    operations = [
        migrations.RemoveField(model_name="user", name="show_age"),
        migrations.RemoveField(model_name="user", name="show_avatar"),
        migrations.RemoveField(model_name="user", name="show_email"),
        migrations.RemoveField(model_name="user", name="show_friends"),
        migrations.RemoveField(model_name="user", name="show_geo"),
        migrations.RemoveField(model_name="user", name="show_media"),
        migrations.RemoveField(model_name="user", name="show_posts"),
        migrations.RemoveField(model_name="user", name="show_social"),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name="Phone"),
        ),
        migrations.AddField(
            model_name="user",
            name="skype",
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name="Skype"),
        ),
    ]
