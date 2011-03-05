# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.mapping.models import Map

class MapSitemap(Sitemap):
    def items(self):
        return Map.objects.all()
    changefreq = 'never'
    priority = 0.5