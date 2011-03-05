# Imports from standard libraries
from datetime import date, datetime, time

# Imports from Django
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import urlize
from django.views.decorators.cache import cache_page

# Imports from brubeck
from brubeck.events.models import Calendar, Event

# Imports from python modules. For now, Calendar and Datetime
import calendar as pycal
from datetime import datetime

def grid_one(request, year=datetime.now().year, month=datetime.now().month, day=None, calendar_slug=None, page=1):
    """
    Shows a grid (similar in appearance to a physical calendar) of upcoming events for either a specific calendar or no 
    calendar at all.
    """
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
    except ValueError:
        raise Http404
    
    calendar = None
    calendar_list = Calendar.objects.all().order_by('name')
    events = Event.objects.all()
    if calendar_slug:
        calendar = get_object_or_404(Calendar, slug=calendar_slug)
        events = events.filter(calendars=calendar)

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

    event_list = events.filter(Q(start__year=year, start__month=month) | Q(end__year=year, end__month=month))
    page_name = "This is a test of the calendaring system."

    page = {
        'calendar': calendar,
        'calendar_list': calendar_list,
        'event_list': event_list,
        'month': month,
        'month_formatted': month_formatted,
        'month_minus': month_minus,
        'month_name': month_name,
        'month_plus': month_plus,
        'page_name': page_name,
        'this_month': this_month,
        'this_year': this_year,
        'today': today,
        'weekday_header': weekday_header,
        'year': year,
        'year_minus': year_minus,
        'year_plus': year_plus,
    }
    
    return render_to_response('events/gridiron.html', page, context_instance=RequestContext(request))

def event_list(request, year=None, month=None, day=None, calendar_slug=None, page=1):
    """
    Shows a list of upcoming events for either a specific calendar or no 
    calendar at all.
    """
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
    
    calendar = None
    events = Event.not_past.all()
    if calendar_slug:
        calendar = get_object_or_404(Calendar, slug=calendar_slug)
        events = events.filter(calendars=calendar)
    
    if not year:
        events = events
        page_name = "Upcoming events"
    elif not month:
        events = events.filter(Q(start__year=year) | Q(end__year=year))
        page_name = "Events in %s" % year
    elif not day:
        events = events.filter(Q(start__year=year, start__month=month) | Q(end__year=year, end__month=month))
        page_name = "Events in %s" % date(year, month, 1).strftime("%B %Y")
    else:
        events = events.filter(Q(start__year=year, start__month=month, start__day=day) | Q(end__year=year, end__month=month, end__day=day))
        #ymd = datetime.date(year, month, day)
        #events = events.filter(Q(start__gte=ymd) & Q(end__lte=ymd))
        page_name = "Events on %s" % date(year, month, day).strftime("%B %d, %Y")
    
    if calendar:
        page_name += " from %s" % calendar
    
    paginator = Paginator(events, 10)
    
    try:
        event_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    page = {
        'calendar': calendar,
        'calendar_slug': calendar_slug,
        'event_page': event_page,
        'page_name': page_name
    }
    
    return render_to_response('events/event_list.html', page, context_instance=RequestContext(request))

def event_detail(request, year=None, month=None, day=None, event_slug=None):
    """
    Shows a specific event.
    """
    try:
        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)
    except ValueError:
        raise Http404
    
    events = Event.objects.filter(start__year=year, start__month=month, start__day=day)
    try:
        event = events.get(slug=event_slug)
    except Event.DoesNotExist:
        raise Http404
    
#    if calendar_slug:
#        return HttpResponsePermanentRedirect(event.get_absolute_url())
    
    page = {
        'event': event
    }
    
    return render_to_response('events/event_detail.html', page, context_instance=RequestContext(request))

