from django.db import migrations


def migration(apps, schema_editor):
    Chat = apps.get_model("chat", "Chat")
    db_alias = schema_editor.connection.alias
    for chat in Chat.objects.using(db_alias):
        last_message = chat.chat_messages.order_by("created_date").last()
        if last_message:
            Chat.objects.filter(pk=chat.pk).update(updated_date=last_message.created_date)


class Migration(migrations.Migration):

    dependencies = [("chat", "0028_auto_20200312_2016")]

    operations = [migrations.RunPython(migration)]
