# Imports from Django
from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.podcasts.models import Channel, Episode

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^episodes/(?P<object_id>\d+)/$', 'object_detail', {'queryset': Episode.objects.all()}, name='podcasts-episode-detail'),
    (r'^episodes/$', 'object_list', {'queryset': Episode.objects.all(), 'extra_context': {'page_title': 'All episodes'}}),
    (r'^archived/$', 'object_list', {'queryset': Channel.old.all(), 'extra_context': {'page_title': 'Archived channels'}}),
#    url(r'^(?P<slug>[-\w]+)/$', 'object_detail', {'queryset': Channel.objects.all(), 'template_name': 'podcasts/episode_list.html'}, name='podcasts-channel-detail'),
#    (r'^$', 'object_list', {'queryset': Channel.current.all(), 'extra_context': {'page_title': 'Current channels'}})
)

urlpatterns += patterns('',
    (r'^calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'brubeck.podcasts.views.calendar_day_view'),
    (r'^calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^calendar/(?P<year>\d{4})/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^calendar/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^(?P<channel_slug>[-\w]+)/calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'brubeck.podcasts.views.calendar_day_view'),
    (r'^(?P<channel_slug>[-\w]+)/calendar/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^(?P<channel_slug>[-\w]+)/calendar/(?P<year>\d{4})/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^(?P<channel_slug>[-\w]+)/calendar/$', 'brubeck.podcasts.views.calendar_view'),
    (r'^(?P<slug>[-\w]+)/$', 'brubeck.podcasts.views.archive_view'),
)

# urlpatterns += patterns('django.views.generic.list_detail',
#     (r'^$', 'object_list', {'queryset': Channel.current.all(), 'extra_context': {'page_title': 'Current channels'}}),
# )

# urlpatterns += patterns('django.views.generic.list_detail',
#     url(r'^(?P<slug>[-\w]+)/$', 'object_detail', {'queryset': Channel.objects.all(), 'template_name': 'podcasts/episode_list.html'}, name='podcasts-channel-detail'),
# )

urlpatterns += patterns('',
    (r'^$', 'brubeck.podcasts.views.list_view'),
)
