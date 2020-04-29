from django.db import migrations
from django.utils.text import slugify


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    User = apps.get_model("users", "User")
    for u in User.objects.all():
        slug = slugify(u.username)
        if User.objects.filter(slug=slug).exclude(pk=u.pk).exists():
            slug = str(u.pk)
        u.slug = slug
        u.save(update_fields=("slug",))


class Migration(migrations.Migration):

    dependencies = [("users", "0014_auto_20190427_2008")]

    operations = [migrations.RunPython(migration)]
