from django.conf.urls.defaults import *

from brubeck.voxpopuli.models import Poll

urlpatterns = patterns('brubeck.voxpopuli.views',
    url(r'^(?P<id>\d+)/results/$', 'poll_results', name='voxpopuli-poll-results'),
    url(r'^(?P<id>\d+)/$', 'poll_vote', name='voxpopuli-poll-vote'),
)

from brubeck.voxpopuli.models import Poll
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^p(?P<page>\d+)/$', 'object_list', {'queryset': Poll.objects.all(), 'paginate_by':10}),
    (r'^$', 'object_list', {'queryset': Poll.objects.all(), 'paginate_by':10}),
)

