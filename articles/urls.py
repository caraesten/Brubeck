# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.articles.views',
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/p(?P<page>\d+)/$', 'archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/images/$', 'detail', {'mode': 'images'}, name='core-articles-images'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'detail', name='core-articles-detail'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'archive'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/p(?P<page>\d+)/$','archive'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$','archive'),
    (r'^(?P<year>\d{4})/p(?P<page>\d+)/$','archive'),
    (r'^(?P<year>\d{4})/$','archive'),
    (r'^p(?P<page>\d+)/$','archive'),
    (r'^$','archive'),
)