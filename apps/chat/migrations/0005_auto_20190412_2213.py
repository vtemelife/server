# Generated by Django 2.1.5 on 2019-04-12 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chat", "0004_auto_20190412_2210")]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="object_id",
            field=models.UUIDField(blank=True, null=True, verbose_name="Object UUID"),
        )
    ]
