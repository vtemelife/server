from django.db import migrations


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    UserFriend = apps.get_model("users", "UserFriend")
    for u in UserFriend.objects.all():
        UserFriend.objects.filter(user=u.user, friend=u.friend).exclude(pk=u.pk).delete()


class Migration(migrations.Migration):

    dependencies = [("users", "0008_auto_20190417_0643")]

    operations = [migrations.RunPython(migration)]
