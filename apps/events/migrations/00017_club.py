from django.db import migrations, models


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Party = apps.get_model("events", "Party")
    Party.objects.all().update(club_id=models.F("object_id"))


class Migration(migrations.Migration):

    dependencies = [("events", "0016_auto_20200216_0749")]

    operations = [migrations.RunPython(migration)]
