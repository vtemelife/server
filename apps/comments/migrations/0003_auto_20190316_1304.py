# Generated by Django 2.1.5 on 2019-03-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("comments", "0002_auto_20190303_2153")]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created date"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="updated_date",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated date"),
        ),
    ]
