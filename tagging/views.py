# Imports from standard libraries
import itertools

# Imports from Django  
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.articles.models import Article
from brubeck.blogs.models import Entry
from brubeck.core.views import normalize_to_datetime
from brubeck.tagging.models import Tag

@cache_page(60 * 10)
def tag_display(request, slug=None):
    """
    Shows all articles and blog entries with a specific tag, sorted by date.
    """
    tag = get_object_or_404(Tag, slug=slug)

    articles = Article.get_published.filter(tags__in=[tag]).distinct()
    blog_entries = Entry.get_published.filter(tags__in=[tag]).distinct()

    # Put the two QuerySets together...
    items = itertools.chain(articles, blog_entries)
    # Turn the iterator into a list that we can then...
    items = list(items)
    # Sort by date, normalizing everything to be datetime objects so we can
    # compare them.
    items.sort(key=lambda x: normalize_to_datetime(x.pub_date), reverse=True)

    page = {
        'items': items,
        'tag': tag  
    }
       
    return render_to_response('tagging/archive.html', page, context_instance=RequestContext(request))
