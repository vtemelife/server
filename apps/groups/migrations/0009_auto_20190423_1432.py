# Generated by Django 2.1.5 on 2019-04-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("groups", "0008_auto_20190423_1423")]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="relationship_theme",
            field=models.CharField(
                choices=[("swing", "Swing"), ("bdsm", "Bdsm")],
                db_index=True,
                max_length=16,
                verbose_name="Relationship themes",
            ),
        )
    ]
