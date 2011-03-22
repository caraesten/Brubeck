# Imports from standard libraries
from datetime import date

# Imports from Django
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page

# Imports from brubeck
from brubeck.comics.models import ComicEpisode, ComicStrip
from brubeck.publishing.models import Issue

@cache_page(60 * 30)
def archive(request, slug=None, year=None, month=None, day=None, page=1):
    """Show a paginated, optionally date-based archive of comic episodes."""
    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)
    
    # The URL pattern for the year-only archive's first page matches the old
    # standard URL for individual episodes (based on episode ID). If the view
    # gets passed a year that makes no sense, assume it's an episode ID and
    # redirect to the detail view.
    if year and year < 2008:  # The year we first had comics online at all.
        episode = ComicEpisode.objects.get(id=year)
        return HttpResponsePermanentRedirect('/comics/%s/%s/%s/%s/%s/' % (episode.strip.slug, episode.pub_date.year, episode.pub_date.month, episode.pub_date.day, episode.id))
    
    strip = ComicStrip.objects.filter(slug=slug)[0]
    images = ComicEpisode.objects.filter(strip__slug=slug)
    
    if not year:
        images = images
        archive_name = "%s" % strip.title
    elif not month:
        images = images.filter(pub_date__year=year)
        archive_name = "%s episodes from %s" % (strip.title, year)
    elif not day:
        images = images.filter(pub_date__year=year, pub_date__month=month)
        archive_name = "%s episodes from %s" % (strip.title, date(year, month, 1).strftime("%B %Y"))
    else:
        images = images.filter(pub_date=date(year, month, day))
        archive_name = "%s episodes from %s" % (strip.title, date(year, month, day).strftime("%B %d, %Y"))
    
    paginator = Paginator(images, 10)
    
    try:
        archive_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    page = {
        'archive_name': archive_name,
        'archive_page': archive_page
    }
    
    return render_to_response('core/archive.html', page, context_instance=RequestContext(request))

@cache_page(60 * 30)
def detail(request, slug=None, year=None, month=None, day=None, id=None):
    """Show a particular episode."""
    # strip = get_object_or_404(ComicStrip, slug=slug)
    
    try:
        id = int(id)
        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)
    except ValueError:
        raise Http404
    
    # Some old URLs only used the episode ID, even though we now consider the
    # date-based form as canonical.
    if not year:
        episode = get_object_or_404(ComicEpisode, strip__slug=slug, id=id)
    else:
        episode = get_object_or_404(ComicEpisode, strip__slug=slug, pub_date__year=year, pub_date__month=month, pub_date__day=day, id=id)
    
    try:
        previous = episode.get_previous_by_pub_date(strip__slug=slug)
    except ComicEpisode.DoesNotExist:
        previous = None
    try:
        next = episode.get_next_by_pub_date(strip__slug=slug)
    except ComicEpisode.DoesNotExist:
        next = None
    
    page = {
        'episode': episode,
        'next': next,
        'previous': previous
    }
    
    return render_to_response('comics/detail.html', page, context_instance=RequestContext(request))

@cache_page(60 * 60 * 24)
def list(request):
    """Lists all strips, past and present."""
    current_strips = ComicStrip.objects.filter(active=True)
    old_strips = ComicStrip.objects.filter(active=False)
    
    page = {
        'current_strips': current_strips,
        'old_strips': old_strips
    }
    
    return render_to_response('comics/list.html', page, context_instance=RequestContext(request))

@cache_page(60 * 30)
def latest_issue(request):
    """
    Shows all comic episodes from the latest issue.
    """
    site = Site.objects.get_current()
    issue = Issue.objects.filter(volume__publication__site=site).filter(online_update=False).latest()
    episodes = issue.comicepisode_set.all()
    
    page = {
        'episodes': episodes
    }
    
    return render_to_response('comics/latest_issue.html', page, context_instance=RequestContext(request))

