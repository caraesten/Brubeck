from tastypie.api import Api
from brubeck.articles.api import ArticleResource
from brubeck.blogs.api import EntryResource,BlogResource
from brubeck.design.api import GraphicResource
from brubeck.photography.api import PhotoResource
from brubeck.tagging.api import TagResource
from brubeck.events.api import EventResource
from brubeck.podcasts.api import PodcastResource,ChannelResource
from brubeck.multimedia.api import AudioResource,VideoResource,SlideshowResource

v1_api = Api(api_name='v1')
v1_api.register(SectionResource())
v1_api.register(IssueResource())

v1_api.register(ArticleResource())
v1_api.register(BlogResource())
v1_api.register(EntryResource())
v1_api.register(GraphicResource())
v1_api.register(PhotoResource())
v1_api.register(EventResource())
v1_api.register(ChannelResource())
v1_api.register(PodcastResource())
v1_api.register(AudioResource())
v1_api.register(VideoResource())
v1_api.register(SlideshowResource())
v1_api.register(TagResource())


urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)