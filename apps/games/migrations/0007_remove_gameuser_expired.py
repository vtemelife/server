# Generated by Django 2.1.5 on 2019-05-18 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("games", "0006_game_rules")]

    operations = [migrations.RemoveField(model_name="gameuser", name="expired")]
