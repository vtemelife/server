# Generated by Django 2.1.5 on 2019-05-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("clubs", "0026_auto_20190507_0700")]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("waiting", "Waiting moderation"), ("approved", "Approved"), ("declined", "Declined")],
                db_index=True,
                max_length=32,
                null=True,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="clubrequest",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("waiting", "Waiting moderation"), ("approved", "Approved"), ("declined", "Declined")],
                db_index=True,
                max_length=32,
                null=True,
                verbose_name="Status",
            ),
        ),
    ]
