# Imports from Django
from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

# Imports from maneater
from brubeck.tagging.models import Tag

# Everything else
urlpatterns = patterns('brubeck.tagging.views',
    (r'^(?P<slug>[-\w]+)/(?P<page>\d+)/$', 'tag_display'),
    url(r'^(?P<slug>[-\w]+)/$', 'tag_display', name='core-tag'),
)

site = Site.objects.get_current()

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', {'queryset': Tag.objects.all()}),
)
