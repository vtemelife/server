# Generated by Django 2.1.5 on 2020-02-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0062_auto_20200217_0751")]

    operations = [
        migrations.AlterField(
            model_name="user", name="name", field=models.CharField(db_index=True, max_length=150, verbose_name="Name")
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.SlugField(max_length=150, unique=True, verbose_name="Username"),
        ),
    ]
