# Imports from standard libraries
from datetime import datetime, time

# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.multimedia.models import AttachedFile, Video, Slideshow

class AttachedFileSitemap(Sitemap):
    def items(self):
        return AttachedFile.objects.all()
    def lastmod(self, obj):
        return datetime.combine(obj.pub_date, time.min)
    changefreq = 'never'
    priority = 0.65

class VideoSitemap(Sitemap):
    def items(self):
        return Video.objects.all()
    def lastmod(self, obj):
        return datetime.combine(obj.pub_date, time.min)
    changefreq = 'never'
    priority = 0.8

class SlideshowSitemap(Sitemap):
    def items(self):
        return Slideshow.objects.all()
    def lastmod(self, obj):
        return datetime.combine(obj.pub_date, time.min)
    changefreq = 'never'
    priority = 0.8

