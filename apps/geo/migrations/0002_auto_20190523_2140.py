# Generated by Django 2.1.5 on 2019-05-23 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("geo", "0001_initial")]

    operations = [
        migrations.AlterUniqueTogether(name="city", unique_together=set()),
        migrations.AlterUniqueTogether(name="region", unique_together=set()),
    ]
