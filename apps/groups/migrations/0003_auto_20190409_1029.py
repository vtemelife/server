# Generated by Django 2.1.5 on 2019-04-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("groups", "0002_auto_20190331_2300")]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="relationship_theme",
            field=models.CharField(
                choices=[("swing", "Swing"), ("bdsm", "Bdsm"), ("virt", "Virt"), ("other", "Other")],
                max_length=16,
                verbose_name="Relationship themes",
            ),
        )
    ]
