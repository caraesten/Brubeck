# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.core.image_views',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<id>\d+)/$', 'detail', name='core-image-detail'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/p(?P<page>\d+)/$', 'archive'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$','archive'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/p(?P<page>\d+)/$','archive'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$','archive'),
    (r'^(?P<year>\d{4})/p(?P<page>\d+)/$','archive'),
    (r'^(?P<year>\d{4})/$','archive'),
    (r'^p(?P<page>\d+)/$','archive'),
    (r'^$','archive'),
)