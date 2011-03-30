# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.blogs.views',
    (r'^archived/$', 'list_blogs', {'archive': True}),
    # Here are some of the calendar URLs:
    (r'^calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'calendar_day_view'),
    (r'^calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'calendar_view'),
    (r'^calendar/(?P<year>\d{4})/$', 'calendar_view'),
    (r'^calendar/$', 'calendar_view'),
    # Here, the date-based navigation.
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/images/$', 'blog_entry', {'mode': 'images'}, name='blogs-entry-images'),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'blog_entry', name='blogs-entry-detail'),
    (r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'blog_date'),
    (r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'blog_date'),
    (r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/$', 'blog_date'),
    # If we have a four-digit page number supplied to this next line, of 
    # course, it'll match the previous line instead and be interpreted as a 
    # year. We don't have to worry about that for quite some time, though.
    (r'^(?P<blog_slug>[-\w]+)/(?P<page>\d+)/$', 'blog_index'),
    # Here are more calendar URLs:
    (r'^(?P<blog_slug>[-\w]+)/calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'calendar_day_view'),
    (r'^(?P<blog_slug>[-\w]+)/calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'calendar_view'),
    (r'^(?P<blog_slug>[-\w]+)/calendar/(?P<year>\d{4})/$', 'calendar_view'),
    (r'^(?P<blog_slug>[-\w]+)/calendar/$', 'calendar_view'),
    # And now, the list views for individual blogs and the front page.
    url(r'^(?P<blog_slug>[-\w]+)/$', 'blog_index', name='blogs-blog-detail'),
    (r'^$', 'list_blogs'),
)
