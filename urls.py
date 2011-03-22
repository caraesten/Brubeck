# Please try to keep this file organized. Ground rules:
#     * Use include() wherever practical.
#     * If, for whatever reason, URL regular expressions start overriding each
#       other, please make a note of it so it's easier to track down any
#       potential bugs later. (This assumes it's intentional. If it isn't, may
#       God have mercy on your soul.)

# Standard URLconf import
from django.conf.urls.defaults import *

# Imports from Django
from django.conf import settings

# Admin site
from django.contrib.gis import admin
admin.autodiscover()

#import mobileadmin
#mobileadmin.autoregister()

urlpatterns = patterns('',
#    (r'^admin/filebrowser/', include('filebrowser.urls')),
#    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
#    (r'^grappelli/', include('grappelli.urls')),
)

#urlpatterns += patterns('',
#    (r'^ma/(.*)', mobileadmin.sites.site.root),
#)

# Core
urlpatterns += patterns('',
    (r'^$', 'brubeck.management.views.render_frontpage'),
    (r'^editorial-cartoons/', include('brubeck.core.image_views.urls'), {'mediatype': 'editorialcartoon'}),
    (r'^graphics/', include('brubeck.core.image_views.urls'), {'mediatype': 'graphic'}),
    (r'^issues/', include('brubeck.core.image_views.urls')),
    (r'^layouts/', include('brubeck.core.image_views.urls'), {'mediatype': 'layout'}),
    (r'^photos/', include('brubeck.core.image_views.urls'), {'mediatype': 'photo'}),
    (r'^section/', include('brubeck.publishing.urls_sections')),
    (r'^staff/', include('brubeck.personnel.urls')),
    (r'^stories/', include('brubeck.articles.urls')),
    (r'^tags/', include('brubeck.tagging.urls')),
    (r'^multimedia/(?P<page>[-\w]+)/$', 'brubeck.multimedia.views.top_multimedia'),
    (r'^multimedia/$', 'brubeck.multimedia.views.top_multimedia'),
    #(r'^top-online/$', 'brubeck.management.views.top_online'),
)

# Multimedia
#     These first three patterns override the first line of the URLconf that's
#     included immediately afterward. This is intentional, since we'd like
#     to use a view other than brubeck.core.image_views.views.detail.
urlpatterns += patterns('brubeck.multimedia.views',
    url(r'^videos/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<id>\d+)/$', 'detail', {'mediatype': 'video'}, name='multimedia-video-detail'),
    url(r'^slideshows/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<id>\d+)/$', 'detail', {'mediatype': 'slideshow'}, name='multimedia-slideshow-detail'),
    url(r'^audio/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<id>\d+)/$', 'detail', {'mediatype': 'audioclip'}, name='multimedia-audioclip-detail'),
)
urlpatterns += patterns('',
    (r'^videos/', include('brubeck.core.image_views.urls'), {'mediatype': 'video'}),
    (r'^slideshows/', include('brubeck.core.image_views.urls'), {'mediatype': 'slideshow'}),
    (r'^audio/', include('brubeck.core.image_views.urls'), {'mediatype': 'audioclip'}),
)

# E-mail forms
#     Usually, the view should be 'handle_form_and_email'. If you'd like to
#     restrict it to staff members, use 'restricted_email' (and set
#     'editor_required' to True if only editors should have access to it).
from django.contrib.sites.models import Site
site = Site.objects.get_current()
site_name = site.name
from brubeck.core.emailing.forms import *
urlpatterns += patterns('brubeck.core.emailing.views',
    (r'^photo-request/$', 'restricted_email', {
        'form': PhotoRequestForm,
        'form_template': 'emailing/photorequest/form.html',
        'message_template': 'emailing/photorequest/message.txt',
        'subject': "Photo request",
        'recipients': [settings.EDITORS['photo']],
        'editor_required': True,
        'uses_captcha': False
    }),
    (r'^about/contact/$', 'handle_form_and_email', {
        'form': SubmissionForm,
        'form_template': 'emailing/submission/form.html',
        'message_template': 'emailing/submission/message.txt',
        'subject': "Submission to %s" % site_name,
        'recipients': [settings.EDITORS['chief']],
        'sender': 'self'
    }),
    (r'^section/forum/send-letter/$', 'handle_form_and_email', {
        'form': LetterToTheEditorForm,
        'form_template': 'emailing/lettertotheeditor/form.html',
        'message_template': 'emailing/lettertotheeditor/message.txt',
        'subject': "Letter to the editor",
        'recipients': [settings.EDITORS['forum']]
    }),
    (r'^system-test/$', 'handle_form_and_email', {
        'form': SystemTestForm,
        'form_template': 'emailing/systemtest/form.html',
        'message_template': 'emailing/systemtest/message.txt',
        'subject': "System test",
        'recipients': [settings.EDITORS['online_dev']]
    }),
)
urlpatterns += patterns('django.views.generic.simple',
    (r'^thanks/$', 'direct_to_template', {'template': 'emailing/thanks.html'}),
)

# Other applications
urlpatterns += patterns('',
    # User controls (using django-registration)
    #(r'^accounts/', include('registration.urls')),
    # Blogs
    (r'^blogs/', include('brubeck.blogs.urls')),
    # Calendar
    (r'^calendar/', include('brubeck.events.urls')),
    # Comments (using django.contrib.comments)
    (r'^comments/', include('django.contrib.comments.urls')),
    # Comics
    (r'^comics/', include('brubeck.comics.urls')),
    # Form to e-mail articles and blog posts
    (r'^email/(?P<content_type>[-\w]+)/(?P<content_id>\d+)/$', 'brubeck.core.emailing.views.email_content'),
    # Game answers
    (r'^games/', include('brubeck.games.urls')),
    # Attached maps
    (r'^maps/', include('brubeck.mapping.urls')),
    # Podcasts
    (r'^podcasts/', include('brubeck.podcasts.urls')),
    # Polls - VIEWS NOT ADDED. COMMENT BACK IN WHEN THEY ARE.
    #(r'^polls/', include('brubeck.voxpopuli.urls_polls')),
    # Reporters' database
    (r'^reporters/', include('brubeck.reporters.urls')),
    # Surveys SEE ABOVE
    #(r'^surveys/', include('brubeck.voxpopuli.urls_surveys')),
)

# Feeds
from brubeck.articles.feeds import ArticleFeed
from brubeck.blogs.feeds import BlogFeed
from brubeck.podcasts.feeds import PodcastFeed
from brubeck.publishing.feeds import SectionFeed
from brubeck.tagging.feeds import TagFeed
feeds = {
    'blogs': BlogFeed,
    'latest': ArticleFeed,
    'podcasts': PodcastFeed,
    'sections': SectionFeed,
    'tags': TagFeed,
}
urlpatterns += patterns('',
    (r'^feeds/$', 'brubeck.syndication.views.feeds'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
