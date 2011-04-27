from tastypie.resources import ModelResource
from brubeck.blogs.models import Entry,Blog
from tastypie import fields
from brubeck.publishing.api import SectionResource

class BlogResource(ModelResource):
	section = fields.ForeignKey(SectionResource, 'blog')
	class Meta:
		queryset = Blog.objects.all()
		resource_name = 'blog'
		allowed_methods = ['get']

class EntryResource(ModelResource):
	blog = fields.ForeignKey(BlogResource, 'blog')
	tag = fields.ToManyField('brubeck.tagging.api.TagResource', 'tag')
	photos = fields.ToManyField('brubeck.photography.api.PhotoResource', 'photos')
	videos = fields.ToManyField('brubeck.multimedia.api.VideoResource', 'videos')
	audio_clips = fields.ToManyField('brubeck.multimedia.api.AudioResource', 'audio_clips')
	slideshows = fields.ToManyField('brubeck.multimedia.api.SlideshowResource', 'slideshows')
	podcast_episodes = fields.ToManyField('brubeck.podcasts.api.PodcastResource', 'podcast_episodes')
	class Meta:
		queryset = Entry.objects.all()
		resource_name = 'entry'
		allowed_methods = ['get']