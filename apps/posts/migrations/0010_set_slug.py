from django.db import migrations
from django.utils.text import slugify


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Post = apps.get_model("posts", "Post")
    for p in Post.objects.all():
        slug = slugify(p.title)
        if Post.objects.filter(slug=slug).exists():
            slug = str(p.pk)
        p.slug = slug
        p.save(update_fields=("slug",))


class Migration(migrations.Migration):

    dependencies = [("posts", "0009_post_slug")]

    operations = [migrations.RunPython(migration)]
