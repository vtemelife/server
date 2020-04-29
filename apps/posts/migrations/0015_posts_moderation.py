from django.db import migrations


def migration(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    Post.objects.filter(status="waiting").update(status=None)


class Migration(migrations.Migration):

    dependencies = [("posts", "0014_auto_20190507_0848")]

    operations = [migrations.RunPython(migration)]
