from tastypie.resources import ModelResource
from brubeck.photography.models import Photo
from brubeck.publishing.api import IssueResource,SectionResource

class PhotoResource(ModelResource):
		issue = fields.ForeignKey(IssueResource, 'issue')
		section = fields.ForeignKey(SectionResource, 'section')
		tag = fields.ToManyField('brubeck.tagging.api.TagResource', 'tag')
        class Meta:
                queryset = Photo.objects.all()
                resource_name = 'photo'
                allowed_methods = ['get']

