from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.mapping.views',
    url(r'^(?P<slug>[-\w]+)/$', 'detail', {'mode': 'page'}, name='mapping-map-detail'),
)

from brubeck.mapping.models import Map
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', {'queryset': Map.objects.all()}),
)

