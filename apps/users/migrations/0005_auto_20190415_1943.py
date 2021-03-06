# Generated by Django 2.1.5 on 2019-04-15 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0004_auto_20190413_1418")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(db_index=True, max_length=150, verbose_name="Username"),
        ),
    ]
