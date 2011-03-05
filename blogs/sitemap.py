# Imports from Django
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.blogs.models import Blog, Entry

site = Site.objects.get_current()

class BlogSitemap(Sitemap):
    def items(self):
        return Blog.objects.filter(section__publication__site=site)
    def lastmod(self, obj):
        try:
            return obj.entry_set.latest().pub_date
        except:
            return None
    changefreq = 'daily'
    priority = 0.5

class EntrySitemap(Sitemap):
    def items(self):
        return Entry.get_published.filter(blog__section__publication__site=site)
    def lastmod(self, obj):
        return obj.pub_date
    changefreq = 'daily'
    priority = 0.75