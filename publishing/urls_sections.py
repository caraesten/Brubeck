# Imports from Django
from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

# Imports from maneater
from brubeck.publishing.models import Section

# Everything else
urlpatterns += patterns('brubeck.publishing.views',
    (r'^(?P<slug>[-\w]+)/archives/(?P<page>\d+)/$', 'section_archive'),
    (r'^(?P<slug>[-\w]+)/archives/$', 'section_archive'),
)

urlpatterns += patterns('brubeck.management.views',
    url(r'^(?P<slug>[-\w]+)/$', 'section_front', name='core-section'),
)

site = Site.objects.get_current()

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', {'queryset': Section.objects.filter(publication__site=site)}),
)
