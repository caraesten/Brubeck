# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.publishing.views',
    (r'^(?P<id>\d+)/(?P<page>\d+)/$', 'issue_detail'),
    url(r'^(?P<id>\d+)/$', 'issue_detail', name='core-issue-detail'),
    (r'^(?P<page>\d+)/$', 'issue_archive'),
    url(r'^$', 'issue_archive', name='core-issue-archive'),
)
