# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.comics.views',
    # Hope you don't get a comic that'll need the slug 'latest'.
    (r'^latest/$', 'latest_issue'),
    
    url(r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<id>\d+)/$', 'detail', name='comic-episode-detail'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/p(?P<page>\d+)/$', 'archive'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'archive'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/p(?P<page>\d+)/$', 'archive'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/p(?P<page>\d+)/$', 'archive'),
    
    # This one actually also matches the earlier ID-based URLs we used to use.
    # The archive view determines whether the user intends the second argument
    # here to be a year or an episode ID and redirects if necessary.
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/$', 'archive'),
    
    (r'^(?P<slug>[-\w]+)/p(?P<page>\d+)/$', 'archive'),
    url(r'^(?P<slug>[-\w]+)/$', 'archive', name='comic-strip-archive'),
    
    (r'^$', 'list'),
)