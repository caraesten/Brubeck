# Imports from standard libraries
from datetime import date

# Imports from Django
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.http import urlencode
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.articles.models import Article
from brubeck.blogs.models import Blog, Entry
from brubeck.management.models import WebFront
from brubeck.multimedia.models import AudioClip, Slideshow, Video
from brubeck.podcasts.models import Channel, Episode
from brubeck.publishing.models import Issue, Section
from brubeck.tagging.models import Tag

@cache_page(60 * 5)
def issue_archive(request, page=1):
    """
    Shows a paginated list of issues.
    """
    try:
        page = int(page)
    except ValueError:
        raise Http404
    
    site = Site.objects.get_current()
    try:
        issues = Issue.objects.filter(volume__publication__site=site)
    except:
        raise Http404
    
    archive_name = 'Issues'
    
    paginator = Paginator(issues, 20)
    
    try:
        archive_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    page = {
        'archive_name': archive_name,
        'archive_page': archive_page
    }
    
    return render_to_response('publishing/archive.html', page, context_instance=RequestContext(request))

@cache_page(60 * 5)
def issue_detail(request, id=None, page=None):
    """
    Shows a specific issue and all its contents.
    """
    issue = get_object_or_404(Issue, id=int(id))
    
    if page:
        HttpResponsePermanentRedirect(issue.get_absolute_url())
    
    images = []
    images.extend(issue.photo_set.all())
    images.extend(issue.graphic_set.all())
    
    comics = issue.comicepisode_set.all()
    games = issue.gameanswer_set.all()
    
    page = {
        'comics': comics,
        'games': games,
        'images': images,
        'issue': issue
    }
    
    return render_to_response('publishing/issue_detail.html', page, context_instance=RequestContext(request))

def section_archive(request, slug=None, page=1):
    """
    Shows a paginated list of articles for a given section.
    """
    site = Site.objects.get_current()
    try:
        section = Section.objects.filter(publication__site=site).get(slug=slug)
    except Section.DoesNotExist:
        raise Http404
    
    archive_name = section.name

    try:
        page = int(page)
    except ValueError:
        raise Http404
     
    articles = Article.get_published.filter(section=section)
    paginator = Paginator(articles, 20)

    try:
        archive_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    next_page_url = '/section/%s/archives/%s/' % (slug, page + 1)
    previous_page_url = '/section/%s/archives/%s/' % (slug, page - 1)
    
    page = {
        'archive_name': archive_name,
        'archive_page': archive_page,
        'next_page_url': next_page_url,
        'previous_page_url': previous_page_url,
        'section': section
    }
        
    return render_to_response('publishing/section_archive.html', page, RequestContext(request))
