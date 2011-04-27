from tastypie.resources import ModelResource
from tastypie import fields
from brubeck.articles.models import Article
from brubeck.publishing.api import SectionResource,IssueResource

class ArticleResource(ModelResource):
	issue = fields.ForeignKey(IssueResource, 'issue')
	section = fields.ForeignKey(SectionResource, 'section')
	tags = fields.ToManyField('brubeck.tagging.api.TagResource', 'tags')
	photos = fields.ToManyField('brubeck.photography.api.PhotoResource', 'photos')
	videos = fields.ToManyField('brubeck.multimedia.api.VideoResource', 'videos')
	audio_clips = fields.ToManyField('brubeck.multimedia.api.AudioResource', 'audio_clips')
	slideshows = fields.ToManyField('brubeck.multimedia.api.SlideshowResource', 'slideshows')
	podcast_episodes = fields.ToManyField('brubeck.podcasts.api.PodcastResource', 'podcast_episodes')
	photos = fields.ToManyField('brubeck.design.api.GraphicResource', 'graphics')
	class Meta:
		queryset = Article.objects.all()
		resource_name = 'article'
		allowed_methods = ['get']
