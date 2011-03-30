from brubeck.tagging.models import Tag
from tastypie.resources import ModelResource

class TagResource(ModelResource):
	class Meta:
		queryset = Tag.objects.all()
		resource_name = 'tag'
		allowed_methods = ['get']
