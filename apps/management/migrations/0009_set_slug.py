from django.db import migrations


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Task = apps.get_model("management", "Task")
    User = apps.get_model("users", "User")
    for task in Task.objects.all():
        if task.params:
            user_pk = task.params.get("user_pk")
            approver_pk = task.params.get("approver_pk")
            if user_pk:
                user = User.objects.filter(pk=user_pk).first()
                if user:
                    task.params["user_slug"] = user.slug
            if approver_pk:
                approver = User.objects.filter(pk=approver_pk).first()
                if approver:
                    task.params["approver_slug"] = approver.slug
            task.save()


class Migration(migrations.Migration):

    dependencies = [("management", "0008_set_slug")]

    operations = [migrations.RunPython(migration)]
