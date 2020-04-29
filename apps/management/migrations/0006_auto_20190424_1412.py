# Generated by Django 2.1.5 on 2019-04-17 06:43

import django.utils.timezone
from django.db import migrations, models


def migration(apps, schema_editor):
    Task = apps.get_model("management", "Task")
    User = apps.get_model("users", "User")
    db_alias = schema_editor.connection.alias
    for user in User.objects.using(db_alias).filter(is_active=True, is_deleted=False, role="guest"):
        Task.objects.create(
            task_type="moderation_guest", params={"user_pk": str(user.pk), "user_username": str(user.username)}
        )

    for user in (
        User.objects.using(db_alias)
        .filter(is_active=True, is_deleted=False, is_real=False)
        .exclude(approver__isnull=True)
    ):
        Task.objects.create(
            task_type="moderation_real",
            params={
                "user_pk": str(user.pk),
                "user_username": str(user.username),
                "approver_pk": str(user.approver.pk),
                "approver_username": str(user.approver.username),
            },
        )


class Migration(migrations.Migration):

    dependencies = [("management", "0005_auto_20190424_1411")]

    operations = [migrations.RunPython(migration)]
