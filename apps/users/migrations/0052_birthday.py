import datetime

from django.db import migrations


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    User = apps.get_model("users", "User")
    for u in User.objects.exclude(birthday__isnull=False).exclude(birthday_second__isnull=False):
        if not u.age:
            continue
        age = u.age.lower().replace(" ", "").replace("/", "").replace("\\", "").replace("-", "")
        if u.age.isdigit():
            u.birthday = datetime.date.today().year - int(u.age)
            u.save(update_fields=("birthday",))
            continue
        m_age = None
        if "м" in age:
            m_age = age.split("м")[1][:2]
        w_age = None
        if "ж" in age:
            w_age = age.split("ж")[1][:2]

        if m_age and m_age.isdigit():
            u.birthday = datetime.date.today().year - int(m_age)
            u.save(update_fields=("birthday",))
        if w_age and w_age.isdigit():
            u.birthday_second = datetime.date.today().year - int(w_age)
            u.save(update_fields=("birthday_second",))


class Migration(migrations.Migration):

    dependencies = [("users", "0051_auto_20190819_2312")]

    operations = [migrations.RunPython(migration)]
