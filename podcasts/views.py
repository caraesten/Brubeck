#  Imports from Django.
from django.contrib.sites.models import Site
from django.views.generic.list_detail import object_list
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import urlize
from django.views.decorators.cache import cache_page

# Imports from brubeck.
from brubeck.podcasts.models import Channel, Episode

# Imports from python modules. For now, Calendar and Datetime
import calendar as pycal
from datetime import datetime

def list_view(request):
    site = Site.objects.get_current()
    channels = Channel.current.filter(section__publication__site=site)
    channel_list = []
    channels_filtered = []
    for channel in channels.all():
        channel_list.append(channel.id)
        for section in channel.section.all():
            if section.publication.site == site:
                channels_filtered.append(channel)
    channels = channels_filtered
    episode_list = Episode.objects.filter(channel__id__in=channel_list).order_by('-pub_date')[:10]
    return object_list(request, episode_list, template_name='podcasts/index.html', extra_context={'page_title': 'Podcasts', 'sidebar': channels})

def archive_view(request, slug):
    site = Site.objects.get_current()
    if slug:
        object = get_object_or_404(Channel, slug=slug)
    else:
        object = None
    channels = Channel.current.all()
    channels_filtered = []
    for channel in channels:
        for section in channel.section.all():
            if section.publication.site == site:
                channels_filtered.append(channel)
#    channels = Channel.current.filter(section__publication__site=site)
    channels = channels_filtered
    page = {
        'channels': channels,
        'object': object,
    }
    return render_to_response('podcasts/episode_list.html', page, context_instance=RequestContext(request))

def calendar_view(request, year=datetime.now().year, month=datetime.now().month, channel_slug=None, page=1):
    """
    Shows a grid (similar in appearance to a physical calendar) of podcasts for either a specific podcast channel or no
    channel at all.  Based on the GridOne layout originally developed for Calendars.
    """
    site = Site.objects.get_current()
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
    except ValueError:
        raise Http404

    channel = None
    channel_list = Channel.current.filter(section__publication__site=site).order_by('title')
    episodes = Episode.objects.filter(channel__section__publication__site=site)
    if channel_slug:
        channel = get_object_or_404(Channel, slug=channel_slug)
        episodes = episodes.filter(channel=channel)

    month_formatted = pycal.monthcalendar(year, month)

    month_minus = month - 1

    month_plus = month + 1

    month_name = pycal.month_name[month]

    weekday_header = pycal.weekheader(3).strip().split(" ")                                              

    year_minus = year - 1

    year_plus = year + 1

    today = datetime.now().day

    this_month = datetime.now().month

    this_year = datetime.now().year

    episode_list = episodes.filter(pub_date__year=year).filter(pub_date__month=month)
    page_name = "This is a test of the calendaring system."

    page = {
        'channel': channel,
        'channel_list': channel_list,
        'episode_list': episode_list,
        'month': month,
        'month_formatted': month_formatted,
        'month_minus': month_minus,
        'month_name': month_name,
        'month_plus': month_plus,
        'page_name': page_name,
        'site': site,
        'this_month': this_month,
        'this_year': this_year,
        'today': today,
        'weekday_header': weekday_header,
        'year': year,
        'year_minus': year_minus,
        'year_plus': year_plus,
    }

    return render_to_response('podcasts/calendar.html', page, context_instance=RequestContext(request))

def calendar_day_view(request, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, channel_slug=None, page=1):
    """
    Shows a grid (similar in appearance to a physical calendar) of podcasts for either a specific podcast channel or no
    channel at all.  Based on the GridOne layout originally developed for Calendars.
    """
    site = Site.objects.get_current()
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
    except ValueError:
        raise Http404

    channel = None
    channel_list = Channel.current.filter(section__publication__site=site).order_by('title')
    episodes = Episode.objects.filter(channel__section__publication__site=site)
    if channel_slug:
        channel = get_object_or_404(Channel, slug=channel_slug)
        episodes = episodes.filter(channel=channel)

    month_formatted = pycal.monthcalendar(year, month)

    month_minus = month - 1

    month_plus = month + 1

    month_name = pycal.month_name[month]

    weekday_header = pycal.weekheader(3).strip().split(" ")                                              

    year_minus = year - 1

    year_plus = year + 1

    today = datetime.now().day

    this_month = datetime.now().month

    this_year = datetime.now().year

    episode_list = episodes.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day)
    page_name = "This is a test of the calendaring system."

    page = {
        'channel': channel,
        'channel_list': channel_list,
        'day': day,
        'episode_list': episode_list,
        'month': month,
        'month_formatted': month_formatted,
        'month_minus': month_minus,
        'month_name': month_name,
        'month_plus': month_plus,
        'page_name': page_name,
        'site': site,
        'this_month': this_month,
        'this_year': this_year,
        'today': today,
        'weekday_header': weekday_header,
        'year': year,
        'year_minus': year_minus,
        'year_plus': year_plus,
    }

    return render_to_response('podcasts/calendarday.html', page, context_instance=RequestContext(request))


