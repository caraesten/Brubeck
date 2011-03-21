# Imports from Django
from django.conf.urls.defaults import *

urlpatterns = patterns('brubeck.personnel.views',
    # Staffers' portfolio pages. Without slug, defaults to active staff list.
    url(r'^view/(?P<slug>[-\w]+)/$', 'detail', name='core-staff-detail'),
    (r'^view/$', 'staffers'),
    # Canonical way to access staff lists. Allows use of 2008 site's
    # /staff/all/ URL.
    url(r'^(?P<mode>[-\w]+)/(?P<page>\d+)/$', 'staffers', name='core-staff-list'),
    (r'^(?P<mode>[-\w]+)/$', 'staffers'),
    # Alternate addresses for active staff list
    (r'^(?P<page>\d+)/$', 'staffers'),
    (r'^$', 'staffers'),
)