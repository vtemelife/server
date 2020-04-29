from django.db import migrations


def migration(apps, schema_editor):
    Chat = apps.get_model("chat", "Chat")
    db_alias = schema_editor.connection.alias
    for chat in Chat.objects.using(db_alias):
        if chat.users.count() == chat.users.filter(role="moderator").count():
            chat.name = "Чат с модераторами"
            chat.chat_type = "chat_with_moderators"
            chat.save(update_fields=("name", "chat_type"))
        elif chat.users.count() == 2:
            chat.name = None
            chat.chat_type = "conversation"
            chat.save(update_fields=("name", "chat_type"))


class Migration(migrations.Migration):

    dependencies = [("chat", "0023_auto_20190422_1623")]

    operations = [migrations.RunPython(migration)]
