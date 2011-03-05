# Imports from standard libraries
from datetime import date, datetime, time
import itertools

# Imports from Django
from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import escape

# Import from brubeck
from brubeck.podcasts.models import Channel, Episode

def list_authors(item):
    """
    Lists reporters according to AP list style. Falls back to a staff credit.
    """
    authors = ''
    byline = item.reporters.all()
    staffers = byline.count()
    if staffers:
        counter = 0
        for staffer in byline:
            if counter != 0:
                if counter == staffers - 1:
                    authors += ' and '
                else:
                    authors += ', '
            authors += escape(staffer)
            counter += 1
    else:
        authors = 'The brubeck staff'

class PodcastFeed(Feed):
    """
    Shows the latest episodes for a given channel (or for all channels if none
    is specified).
    """
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        elif len(bits) == 1:
            return Channel.objects.filter(slug=bits[0])
        else:
            return Channel.objects.all()
    
    def title(self, obj):
        if obj.count() > 1:
            return "All podcasts"
        else:
            return obj[0].title
    
    def link(self, obj):
        if obj.count() > 1:
            return '/feeds/podcasts/'
        else:
            return '/feeds/podcasts/%s/' % obj[0].slug
    
    def description(self, obj):
        if obj.count() > 1:
            return "The latest news and updates from the official student newspaper of the University of Missouri."
        else:
            return obj[0].description
    
    author_name = "The brubeck"
    author_email = "online@thebrubeck.com"
    categories = ('news', 'college', 'university', 'student news', 'student newspaper', 'missouri', 'mizzou', 'university of missouri', 'brubeck')
    copyright = "Copyright &xa9; %s The brubeck Student Newspaper" % date.today().year
    
    def items(self, obj):
        return Episode.objects.filter(channel__in=obj)[:10]
    
    def item_link(self, item):
        return '/podcasts/episodes/%s/' % item.id
    
    def item_author_name(self, item):
        return list_authors(item)
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_copyright(self, item):
        return "Copyright &xa9; %s The brubeck Student Newspaper" % item.pub_date.year
    
    def item_enclosure_url(self, item):
        return item.file.url
    
    def item_enclosure_length(self, item):
        return item.file.size
    
    def item_enclosure_mime_type(self, item):
        return item.get_mime_type()

