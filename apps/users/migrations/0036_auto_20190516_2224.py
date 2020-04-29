# Generated by Django 2.1.5 on 2019-05-16 22:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0035_auto_20190515_1111")]

    operations = [
        migrations.AlterModelOptions(
            name="useronline", options={"verbose_name": "User Online", "verbose_name_plural": "Users Online"}
        ),
        migrations.AlterField(
            model_name="user",
            name="relationship_formats",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("open_swing", "Open Swing"),
                        ("close_swing", "Close Swing"),
                        ("soft_swing", "Soft Swing"),
                        ("wmw", "WMW"),
                        ("mwm", "MWM"),
                        ("sexwife", "Sexwife"),
                        ("hotwife", "Hotwife"),
                        ("cuckold", "Cuckold"),
                        ("cuckqueen", "Cuckqueen"),
                        ("top", "Top"),
                        ("bottom", "Bottom"),
                        ("switch", "Switch"),
                        ("lgbt_active", "Active"),
                        ("lgbt_passive", "Passive"),
                        ("lgbt_switch", "LGBT Switch"),
                        ("format_poliamoria", "Poliamoria"),
                        ("format_virt", "Virt"),
                        ("format_other", "Other"),
                    ],
                    max_length=16,
                ),
                null=True,
                size=None,
                verbose_name="Relationship formats",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="relationship_themes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("swing", "Swing"),
                        ("bdsm", "Bdsm"),
                        ("virt", "Virt"),
                        ("lgbt", "LGBT"),
                        ("poliamoria", "Poliamoria"),
                        ("other", "Other"),
                    ],
                    max_length=16,
                ),
                null=True,
                size=None,
                verbose_name="Relationship themes",
            ),
        ),
    ]
