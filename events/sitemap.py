# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.events.models import Calendar, Event

class CalendarSitemap(Sitemap):
    def items(self):
        return Calendar.objects.all()
    def lastmod(self, obj):
        return obj.event_set.latest('start').start
    changefreq = 'daily'
    priority = 0.75

class EventSitemap(Sitemap):
    def items(self):
        return Event.objects.all()
    def lastmod(self, obj):
        return obj.start
    changefreq = 'never'
    priority = 0.8