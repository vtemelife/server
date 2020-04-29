from django.db import migrations


def migration(apps, schema_editor):
    Media = apps.get_model("media", "Media")
    Media.objects.filter(status="waiting").update(status=None)


class Migration(migrations.Migration):

    dependencies = [("media", "0017_auto_20190507_0848")]

    operations = [migrations.RunPython(migration)]
