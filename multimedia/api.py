from tastypie.resources import ModelResource
from tastypie import fields
from brubeck.multimedia.models import AudioClip,Slideshow,Video

class AudioResource(ModelResource):
		tag = fields.ToManyField('brubeck.tagging.api.TagResource', 'tag')
		class Meta:
			queryset = AudioClip.objects.all()
			resource_name = 'audioclip'
			allowed_methods = ['get']

class SlideshowResource(ModelResource):
		tag = fields.ToManyField('brubeck.tagging.api.TagResource', 'tag')
		class Meta:
			queryset = Slideshow.objects.all()
			resource_name = 'slideshow'
			allowed_methods = ['get']

class VideoResource(ModelResource):
		tag = fields.ToManyField('brubeck.tagging.api.TagResource', 'tag')
		class Meta:
			queryset = Video.objects.all()
			resource_name = 'video'
			allowed_methods = ['get']
