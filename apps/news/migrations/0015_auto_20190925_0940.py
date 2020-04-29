# Generated by Django 2.1.5 on 2019-09-25 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("news", "0014_auto_20190924_0605")]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="news_type",
            field=models.CharField(
                choices=[
                    ("site_news", "Hot News"),
                    ("media", "VTeme: New Media"),
                    ("articles", "VTeme: New Articles"),
                    ("friends_media", "Friends: New Media"),
                    ("friends_article", "Friends: New Articles"),
                    ("friends_info", "Friends: Profile Changes"),
                    ("groups_media", "Groups: New Media"),
                    ("groups_article", "Groups: New Articles"),
                    ("clubs_media", "Clubs: New Media"),
                    ("clubs_article", "Clubs: New Articles"),
                    ("clubs_events", "Clubs: Events"),
                ],
                max_length=16,
                verbose_name="Type",
            ),
        )
    ]
