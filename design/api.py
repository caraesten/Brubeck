from tastypie.resources import ModelResource
from brubeck.design.models import Graphic
from brubeck.publishing.api import IssueResource,SectionResource

class GraphicResource(ModelResource):
		issue = fields.ForeignKey(IssueResource, 'issue')
		section = fields.ForeignKey(SectionResource, 'section')
		class Meta:
			queryset = Graphic.objects.all()
			resource_name = 'graphic'
			allowed_methods = ['get']

