# Generated by Django 2.1.5 on 2019-05-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("clubs", "0028_auto_20190513_2139")]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="relationship_theme",
            field=models.CharField(
                choices=[
                    ("swing", "Swing"),
                    ("bdsm", "Bdsm"),
                    ("virt", "Virt"),
                    ("poliamoria", "Poliamoria"),
                    ("other", "Other"),
                ],
                db_index=True,
                max_length=16,
                verbose_name="Relationship themes",
            ),
        )
    ]
