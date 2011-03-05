# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.comics.models import ComicStrip, ComicEpisode

class StripSitemap(Sitemap):
    def items(self):
        return ComicStrip.objects.all()
    def lastmod(self, obj):
        return obj.comicepisode_set.latest().pub_date
    changefreq = 'weekly'
    priority = 0.3

class EpisodeSitemap(Sitemap):
    def items(self):
        return ComicEpisode.objects.all()
    def lastmod(self, obj):
        return obj.pub_date
    changefreq = 'never'
    priority = 0.3