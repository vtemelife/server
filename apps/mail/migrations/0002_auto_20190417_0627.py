# Generated by Django 2.1.5 on 2019-04-17 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("mail", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="email", name="status"),
        migrations.AddField(
            model_name="email",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Is deleted"),
        ),
    ]
