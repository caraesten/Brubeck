"""Image views

Allow users to view images (photos, graphics and layouts) both on their own and
in various lists.

"""

# Imports from standard libraries
from datetime import date

# Imports from Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib.sites.models import Site
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.comics.models import ComicEpisode, EditorialCartoon
from brubeck.design.models import Graphic, Layout
from brubeck.multimedia.models import AudioClip, Slideshow, Video
from brubeck.photography.models import Photo

@cache_page(60 * 5)
def archive(request, year=None, month=None, day=None, page=1, mediatype=None):
    """View a paginated list of images by year, month or day."""
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)
    except ValueError:
        raise Http404
    
    site = Site.objects.get_current()
    
    try:
        if mediatype == 'photo':
            images = Photo.objects.filter(section__publication__site=site)
            url_base = '/photos/'
        elif mediatype == 'editorialcartoon':
            images = EditorialCartoon.objects.filter(section__publication__site=site)
            url_base = '/editorial-cartoons/'
        elif mediatype == 'graphic':
            images = Graphic.objects.filter(section__publication__site=site)
            url_base = '/graphics/'
        elif mediatype == 'layout':
            images = Layout.objects.filter(section__publication__site=site)
            url_base = '/layouts/'
        elif mediatype == 'slideshow':
            images = Slideshow.objects.filter(publication__site=site)
            url_base = '/slideshows/'
        elif mediatype == 'video':
            images = Video.objects.filter(publication__site=site)
            url_base = '/videos/'
        elif mediatype == 'audioclip':
            images = AudioClip.objects.filter(publication__site=site)
            url_base = '/audio/'
        else:
            raise StandardError("mediatype should be 'photo', 'graphic', 'layout', 'slideshow', 'video' or 'audioclip'")
    except:
        raise Http404
    
    mediatype = mediatype.capitalize()
    if mediatype == 'Audioclip':
        mediatype = "Audio clip"
    elif mediatype == 'Editorialcartoon':
        mediatype = "Editorial cartoon"
    
    if not year:
        images = images
        archive_name = "%s " % mediatype
    elif not month:
        images = images.filter(pub_date__year=year)
        archive_name = "%ss from %s" % (mediatype, year)
    elif not day:
        images = images.filter(pub_date__year=year, pub_date__month=month)
        archive_name = "%ss from %s" % (mediatype, date(year, month, 1).strftime("%B %Y"))
    else:
        images = images.filter(pub_date=date(year, month, day))
        archive_name = "%ss from %s" % (mediatype, date(year, month, day).strftime("%B %d, %Y"))
    
    paginator = Paginator(images, 10)
    
    try:
        archive_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    if year:
        url_base += '%s/' % year
    if month:
        url_base += '%s/' % month
    if day:
        url_base += '%s/' % day
    
    next_page_url = '%sp%s/' % (url_base, page + 1)
    previous_page_url = '%sp%s/' % (url_base, page - 1)
    
    page = {
        'archive_name': archive_name,
        'archive_page': archive_page,
        'next_page_url': next_page_url,
        'previous_page_url': previous_page_url
    }
    
    return render_to_response('core/image_archives/archive.html', page, context_instance=RequestContext(request))

@cache_page(60 * 5)
def detail(request, year=None, month=None, day=None, id=None, mediatype=None):
    """View a particular image."""
    site = Site.objects.get_current()
    # From an optimization standpoint, it makes no real sense to convert year,
    # month and day to integers outside the try/except block; since only one
    # mediatype can be chosen at any given time, this conversion will only
    # happen once anyway.
    try:
        if mediatype == 'photo':
            # image = Photo.objects.filter(section__publication__site=site).filter(pub_date=date(int(year), int(month), int(day))).get(id=int(id))
            image = Photo.objects.get(id=int(id))
        elif mediatype == 'editorialcartoon':
            # image = EditorialCartoon.objects.filter(section__publication__site=site).filter(pub_date=date(int(year), int(month), int(day))).get(id=int(id))
            image = EditorialCartoon.objects.get(id=int(id))
        elif mediatype == 'graphic':
            # image = Graphic.objects.filter(section__publication__site=site).filter(pub_date=date(int(year), int(month), int(day))).get(id=int(id))
            image = Graphic.objects.get(id=int(id))
        elif mediatype == 'layout':
            # image = Layout.objects.filter(section__publication__site=site).filter(pub_date=date(int(year), int(month), int(day))).get(id=int(id))
            image = Layout.objects.get(id=int(id))
        else:
            raise StandardError("mediatype should be 'photo', 'graphic' or 'layout'")
    except ObjectDoesNotExist, ValueError:
        raise Http404
    
    page = {
        'image': image
    }
    
    return render_to_response('core/image_archives/detail.html', page, context_instance=RequestContext(request))
