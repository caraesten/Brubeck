# Imports from standard libraries
from datetime import date

# Imports from Django
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template.defaultfilters import escape

# Import from brubeck
from brubeck.blogs.models import Blog, Entry

class BlogFeed(Feed):
    """
    Shows the latest entries for a given blog (or for all blogs if none is
    specified).
    """
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        elif len(bits) == 1:
            return Blog.objects.filter(slug=bits[0])
        else:
            return Blog.objects.all()
    
    def title(self, obj):
        if obj.count() > 1:
            return "All blogs"
        else:
            return obj[0].title
    
    def link(self, obj):
        if obj.count() > 1:
            return '/feeds/blogs/'
        else:
            try:
                return '/feeds/blogs/%s' % obj[0].slug
            except:
                raise Http404
    
    def description(self, obj):
        if obj.count() > 1:
            return "The latest blog posts from the official student newspaper of the University of Missouri."
        else:
            return obj[0].description
    
    author_name = "The brubeck"
    author_email = "online@thebrubeck.com"
    categories = ('news', 'college', 'university', 'student news', 'student newspaper', 'missouri', 'mizzou', 'university of missouri', 'brubeck')
    copyright = "Copyright &xa9; %s The brubeck Student Newspaper" % date.today().year
    
    def items(self, obj):
        return Entry.get_published.filter(blog__in=obj)[:20]
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        if item.byline:
            return item.byline
        elif item.static_byline:
            return item.static_byline
        else:
            return 'The brubeck staff'
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_copyright(self, item):
        return "Copyright &xa9; %s The brubeck Student Newspaper" % item.pub_date.year

