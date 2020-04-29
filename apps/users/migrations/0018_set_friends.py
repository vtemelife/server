from django.db import migrations
from django.utils.text import slugify


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    UserFriend = apps.get_model("users", "UserFriend")
    FriendRequest = apps.get_model("users", "FriendRequest")
    for uf in UserFriend.objects.all():
        if UserFriend.objects.filter(friend=uf.user, user=uf.friend).exists():
            uf.user.friends.add(uf.friend)
            uf.friend.friends.add(uf.user)
        else:
            FriendRequest.objects.create(user=uf.user, friend=uf.friend)


class Migration(migrations.Migration):

    dependencies = [("users", "0017_auto_20190428_1040")]

    operations = [migrations.RunPython(migration)]
