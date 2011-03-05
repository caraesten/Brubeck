import datetime
from haystack import indexes
from haystack.sites import site
from brubeck.mapping.models import Map, Place

class MapIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
    section = indexes.CharField(model_attr='section')
    section_exact = indexes.CharField(model_attr='section', indexed=False)
#    description = indexes.CharField(model_attr='description')
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(MapIndex, self).prepare(object)
#        self.prepared_data['places_addresses'] = [mpl.place.address for mpl in object.mapplacelink_set.all()]
#        self.prepared_data['places_names'] = [mpl.place.name for mpl in object.mapplacelink_set.all()]
#        self.prepared_data['place_information'] = [mpl.additional_info for mpl in object.mapplacelink_set.all()]
#        self.prepared_data['place_web_sites'] = [mpl.web_site for mpl in object.mapplacelink_set.all()]
#        return self.prepared_data

    def prepare_publication(self, object):
        return object.section.publication.name
        
    def prepare_publication_exact(self, object):
        return object.section.publication.name

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Map.objects.all()

site.register (Map, MapIndex)

class PlaceIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    name = indexes.CharField(model_attr='name')
#    address = indexes.CharField(model_attr='address')

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(PlaceIndex, self).prepare(object)
#        return self.prepared_data

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Place.objects.all()

site.register (Place, PlaceIndex)
