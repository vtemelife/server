# Generated by Django 2.1.5 on 2019-04-17 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chat", "0017_auto_20190417_1236")]

    operations = [
        migrations.RemoveField(model_name="conversation", name="creator"),
        migrations.RemoveField(model_name="conversation", name="user"),
        migrations.AddField(
            model_name="message",
            name="chat",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="chat.Chat", verbose_name="Chat"
            ),
        ),
        migrations.DeleteModel(name="Conversation"),
    ]
