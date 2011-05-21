from django.conf.urls.defaults import *

from brubeck.voxpopuli.models import Survey

urlpatterns = patterns('brubeck.voxpopuli.views',
    url(r'^(?P<slug>[-\w]+)/results/$', 'survey_results', name='voxpopuli-survey-results'),
    url(r'^(?P<slug>[-\w]+)/$', 'survey_detail', name='voxpopuli-survey-detail'),
)

from brubeck.voxpopuli.models import Survey
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^p(?P<page>\d+)/$', 'object_list', {'queryset': Survey.objects.all(), 'paginate_by':10}),
    (r'^$', 'object_list', {'queryset': Survey.objects.all(), 'paginate_by':10}),
)
