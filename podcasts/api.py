from tastypie.resources import ModelResource
from brubeck.podcasts.models import Episode,Channel

class ChannelResource(ModelResource):
        class Meta:
                queryset = Channel.objects.all()
                resource_name = 'channel'
                allowed_methods = ['get']



class PodcastResource(ModelResource):
		channel = fields.ForeignKey(ChannelResource, 'channel')
        class Meta:
                queryset = Episode.objects.all()
                resource_name = 'podcast'
                allowed_methods = ['get']

