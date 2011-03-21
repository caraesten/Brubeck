# Imports from standard libraries
from datetime import date, datetime, time

# Imports from Django
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.template.defaultfilters import escape

# Import from maneater
from brubeck.articles.models import Article
from brubeck.publishing.models import Section

def list_authors(item):
    """
    Lists any staff members in the byline according to AP list style. Falls
    back to the static byline and then simply to a staff credit.
    """
    authors = ''
    byline = item.byline.all()
    if byline:
        staffers = byline.count()
        counter = 1
        for staffer in byline:
            if counter != 1:
                if counter == staffers:
                    authors += ' and '
                else:
                    authors += ', '
            authors += escape(staffer)
            counter += 1
    elif item.static_byline:
        authors = item.static_byline
    else:
        authors = 'The Maneater Staff'
    return authors

class SectionFeed(Feed):
    """
    Lists the latest articles from a particular section.
    """
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Section.objects.get(slug=bits[0])
    
    def title(self, obj):
        return "The Maneater - %s" % obj.name
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return '/feeds/sections/%s/' % obj.slug
    
    def description(self, obj):
        return "The latest articles in %s from themaneater.com." % obj.name
    
    author_name = "The Maneater"
    author_email = 'online@themaneater.com'
    categories = ('news', 'college', 'university', 'student news', 'student newspaper', 'missouri', 'mizzou', 'university of missouri', 'maneater')
    copyright = "Copyright &xa9; %s The Maneater Student Newspaper" % date.today().year
    
    def items(self, obj):
        return Article.get_published.filter(section=obj)[:30]
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        return list_authors(item)
    
    def item_pubdate(self, item):
        return datetime.combine(item.pub_date, time.min)
    
    def item_copyright(self, item):
        return "Copyright &xa9; %s The Maneater Student Newspaper" % item.pub_date.year