import uuid
from random import randrange

from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def migration(apps, schema_editor):
    User = apps.get_model("users", "User")
    for u in User.objects.all():
        if is_valid_uuid(u.username):
            username = slugify(unidecode(u.name))
            new_username = username
            while User.objects.filter(username=new_username).exists():
                new_username = username + str(randrange(100))
            u.username = new_username
            u.save(update_fields=("username",))


class Migration(migrations.Migration):

    dependencies = [("users", "0063_auto_20200217_1741")]

    operations = [migrations.RunPython(migration)]
