# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('maneater.polls.views',
    (r'^(?P<id>\d+)/results/$', 'detail', {'show_results': True}),
    url(r'^(?P<id>\d+)/$', 'detail', name='polls-poll-detail'),
)

from brubeck.voxpopuli.models import Poll
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^p(?P<page>\d+)/$', 'object_list', {'queryset': Poll.objects.all(), 'paginate_by':10}),
    (r'^$', 'object_list', {'queryset': Poll.objects.all(), 'paginate_by':10}),
)

