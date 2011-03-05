# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.podcasts.models import Channel, Episode

site = Site.objects.get_current()

class ChannelSitemap(Sitemap):
    def items(self):
        return Channel.objects.filter(section__publication__site=site)
    def lastmod(self, obj):
        return obj.episode_set.latest().pub_date
    changefreq = 'daily'
    priority = 0.5

class EpisodeSitemap(Sitemap):
    def items(self):
        return Episode.objects.all()
    def lastmod(self, obj):
        return obj.pub_date
    changefreq = 'never'
    priority = 0.75