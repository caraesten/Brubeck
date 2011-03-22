# Imports from Django
from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.publishing.models import Issue
from brubeck.games.models import GameAnswer

site = Site.objects.get_current()
try:
	latest_issue = Issue.objects.filter(volume__publication__site=site).filter(online_update=False).latest()
	urlpatterns = patterns('django.views.generic.list_detail',
		url(r'^(?P<object_id>\d+)/$', 'object_detail', {'queryset': GameAnswer.objects.all()}, name='games-answer-detail'),
		(r'^$', 'object_list', {'queryset': GameAnswer.objects.filter(issue=latest_issue)}),
	)
except:
	urlpatterns = patterns('django.views.generic.list_detail',
		url(r'^(?P<object_id>\d+)/$', 'object_detail', {'queryset': GameAnswer.objects.all()}, name='games-answer-detail'),
	)