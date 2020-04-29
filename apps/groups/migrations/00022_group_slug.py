from django.db import migrations, models
from django.utils.text import slugify
from unidecode import unidecode


def migration(apps, schema_editor):
    Group = apps.get_model("groups", "Group")
    for p in Group.objects.all():
        slug = slugify(unidecode(p.name))
        if Group.objects.filter(slug=slug).exists():
            slug = str(p.pk)
        p.slug = slug
        p.save(update_fields=("slug",))


class Migration(migrations.Migration):

    dependencies = [("groups", "0021_auto_20200216_0805")]

    operations = [migrations.RunPython(migration)]
