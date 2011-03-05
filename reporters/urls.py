# Imports from Django
from django.conf.urls.defaults import *

# Imports from brubeck
from brubeck.reporters.models import InfoPage, SourceType

urlpatterns = patterns('brubeck.reporters.views',
    url(r'^info_pages/(?P<slug>[-\w]+)/$', 'staff_object_detail', {'queryset': InfoPage.objects.all()}, name='reporters-infopage-detail'),
    (r'^info_pages/$', 'staff_object_list', {'queryset': InfoPage.objects.all()}),
    url(r'^sources/(?P<type_slug>[-\w]+)/$', 'source_list', name='reporters-source-list'),
    (r'^sources/$', 'staff_object_list', {'queryset': SourceType.objects.all()}),
    (r'^$', 'index_page'),
)