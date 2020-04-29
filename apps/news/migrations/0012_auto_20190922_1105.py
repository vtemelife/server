# Generated by Django 2.1.5 on 2019-09-22 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("news", "0011_auto_20190922_1043")]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="news_type",
            field=models.CharField(
                choices=[
                    ("site_news", "Site news"),
                    ("media", "Media"),
                    ("articles", "Articles"),
                    ("friends_media", "Friends Media"),
                    ("friends_article", "Friends Article"),
                    ("clubs_events", "Clubs Events"),
                ],
                max_length=16,
                verbose_name="Type",
            ),
        )
    ]
