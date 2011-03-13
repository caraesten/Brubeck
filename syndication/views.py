# Imports from Django
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

# Imports from Brubeck
from brubeck.blogs.models import Blog
from brubeck.podcasts.models import Channel
from brubeck.publishing.models import Section

def feeds(request):
    """
    Shows a list of all subdivisions of the site that have associated RSS feeds.
    """
    site = Site.objects.get_current()
    sections = Section.objects.filter(publication__site=site)
    blogs = Blog.current.all()
    podcasts = Channel.current.all()

    page = {
        'blogs': blogs,
        'podcasts': podcasts,
        'sections': sections
    }

    return render_to_response('syndication/feed_list.html', page, context_instance=RequestContext(request))
