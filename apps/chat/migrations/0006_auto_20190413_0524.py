# Generated by Django 2.1.5 on 2019-04-13 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("chat", "0005_auto_20190412_2213")]

    operations = [
        migrations.AlterModelOptions(name="chat", options={"verbose_name": "Chat", "verbose_name_plural": "Chats"}),
        migrations.AlterModelOptions(
            name="message", options={"verbose_name": "Message", "verbose_name_plural": "Messages"}
        ),
    ]
