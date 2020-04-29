from django.db import migrations


def migration(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(is_real=True, status="waiting").update(status="approved")
    User.objects.exclude(role="guest").filter(status="waiting").update(status="approved")
    User.objects.filter(role="guest").update(status="waiting")


class Migration(migrations.Migration):

    dependencies = [("users", "0029_auto_20190507_0848")]

    operations = [migrations.RunPython(migration)]
