from django.db import migrations


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    User = apps.get_model("users", "User")
    Media = apps.get_model("media", "Media")
    MediaFolder = apps.get_model("media", "MediaFolder")
    ContentType = apps.get_model("contenttypes", "ContentType")

    ct_user = ContentType.objects.get_for_model(User)
    ct_media_folder = ContentType.objects.get_for_model(MediaFolder)
    db_alias = schema_editor.connection.alias
    for media in Media.objects.using(db_alias).all():
        if media.content_type == ct_user:
            media_folder, _ = MediaFolder.objects.using(db_alias).get_or_create(
                name="Мои Медиа", creator_id=media.object_id
            )
            media.object_id = media_folder.pk
            media.content_type = ct_media_folder
            media.save(update_fields=("object_id", "content_type"))


class Migration(migrations.Migration):

    dependencies = [("media", "0012_auto_20190505_1342")]

    operations = [migrations.RunPython(migration)]
