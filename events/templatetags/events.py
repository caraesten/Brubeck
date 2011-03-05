from django import template

import datetime

from brubeck.events.models import Event

register = template.Library()

@register.inclusion_tag('events/render_calendar.html')
def render_calendar(id=None):
    id = int(id)

    events = Event.objects.filter(calendars__id=id)

    dates = [datetime.date(2010, 2, 25), datetime.date(2010, 2, 26), datetime.date(2010, 2, 27), datetime.date(2010, 2, 28)]

    events_by_day = []

    for date in dates:
        startday = datetime.datetime.combine(date, datetime.time.min)
        endday = datetime.datetime.combine(date, datetime.time.max)
        events_today = events.filter(start__lte=endday).filter(end__gte=startday)
        events_by_day.append((date, events_today))

    return {
        'events_by_day': events_by_day,
    }
