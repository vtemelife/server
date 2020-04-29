from django.db import migrations, models
from django.utils.text import slugify
from unidecode import unidecode


def migration(apps, schema_editor):
    Club = apps.get_model("clubs", "Club")
    for p in Club.objects.all():
        slug = slugify(unidecode(p.name))
        if Club.objects.filter(slug=slug).exists():
            slug = str(p.pk)
        p.slug = slug
        p.save(update_fields=("slug",))


class Migration(migrations.Migration):

    dependencies = [("clubs", "0039_auto_20200216_0805")]

    operations = [migrations.RunPython(migration)]
