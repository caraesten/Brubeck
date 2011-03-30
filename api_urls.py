from tastypie.api import Api
from brubeck.articles.api import ArticleResource
from brubeck.blogs.api import EntryResource
from brubeck.events.api import EventResource
from brubeck.podcasts.api import PodcastResource
from brubeck.multimedia.api import AudioResource,VideoResource,SlideshowResource

v1_api = Api(api_name='v1')
v1_api.register(ArticleResource())
v1_api.register(EntryResource())
v1_api.register(EventResource())
v1_api.register(PodcastResource())
v1_api.register(AudioResource())
v1_api.register(VideoResource())
v1_api.register(SlideshowResource())


urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)