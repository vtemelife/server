from django.db import migrations


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Club = apps.get_model("clubs", "Club")
    for c in Club.objects.all():
        if c.latitude and c.longitude:
            c.geo = {"coordinates": [c.latitude, c.longitude]}
            c.save(update_fields=("geo",))


class Migration(migrations.Migration):

    dependencies = [("clubs", "0035_auto_20191004_1334")]

    operations = [migrations.RunPython(migration)]
