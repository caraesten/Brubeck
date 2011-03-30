from tastypie.resources import ModelResource
from brubeck.publishing.models import Section,Issue

class SectionResource(ModelResource):
	class Meta:
		queryset = Section.objects.all()
		resource_name = 'section'
		allowed_methods = ['get']

class IssueResource(ModelResource):
	class Meta:
		queryset = Issue.objects.all()
		resource_name = 'issue'
		allowed_methods = ['get']
