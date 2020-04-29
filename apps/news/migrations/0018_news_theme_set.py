from django.db import migrations
from django.utils.text import slugify

TYPE_SITE_NEWS = "site_news"
TYPE_MEDIA = "media"
TYPE_ARTICLES = "articles"
TYPE_FRIENDS_MEDIA = "friends_media"
TYPE_FRIENDS_ARTICLE = "friends_article"
TYPE_FRIENDS_INFO = "friends_info"
TYPE_GROUPS_MEDIA = "groups_media"
TYPE_GROUPS_ARTICLE = "groups_article"
TYPE_CLUBS_MEDIA = "clubs_media"
TYPE_CLUBS_ARTICLE = "clubs_article"
TYPE_CLUBS_EVENTS = "clubs_events"

THEME_SWING = "swing"
THEME_SWING_HISTORY = "swing_history"
THEME_BDSM = "bdsm"
THEME_BDSM_HISTORY = "bdsm_history"
THEME_LGBT = "lgbt"
THEME_LGBT_HISTORY = "lgbt_history"

T_THEME_SWING = "swing"
T_THEME_BDSM = "bdsm"
T_THEME_VIRT = "virt"
T_THEME_LGBT = "lgbt"
T_THEME_POLIAMORIA = "poliamoria"
T_THEME_OTHER = "other"


def migration(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    News = apps.get_model("news", "News")
    Post = apps.get_model("posts", "Post")
    for obj in News.objects.filter(news_type=TYPE_ARTICLES):
        parent = Post.objects.filter(pk=obj.object_id).first()
        if not parent:
            continue
        theme = None
        if parent.theme in (THEME_BDSM, THEME_BDSM_HISTORY):
            theme = T_THEME_BDSM
        elif parent.theme in (THEME_LGBT, THEME_LGBT_HISTORY):
            theme = T_THEME_LGBT
        elif parent.theme in (THEME_SWING, THEME_SWING_HISTORY):
            theme = T_THEME_SWING
        if theme:
            obj.theme = theme
            obj.save(update_fields=("theme",))


class Migration(migrations.Migration):

    dependencies = [("news", "0017_news_theme"), ("posts", "0001_initial")]

    operations = [migrations.RunPython(migration)]
