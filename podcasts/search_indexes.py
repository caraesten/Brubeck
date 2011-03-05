import datetime
from haystack import indexes
from haystack.sites import site
from brubeck.podcasts.models import Channel, Episode

class ChannelIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
#    description = indexes.CharField(model_attr='description')
#    keywords = indexes.CharField(model_attr='keywords')
    section = indexes.MultiValueField()
    section_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.MultiValueField()
    publication_exact = indexes.MultiValueField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(ChannelIndex, self).prepare(object)
#        return self.prepared_data

    def prepare_section(self, object):
        sections = []
        for section in object.section.all():
            sections.append(section)
        return sections
        
    def prepare_section_exact(self, object):
        sections = []
        for section in object.section.all():
            sections.append(section)
        return sections

    def prepare_publication(self, object):
        publications = []
        for section in object.section.all():
            publications.append(section.publication.name)
        return publications
        
    def prepare_publication_exact(self, object):
        publications = []
        for section in object.section.all():
            publications.append(section.publication.name)
        return publications

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Channel.objects.all()

site.register (Channel, ChannelIndex)

class EpisodeIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    channel = indexes.CharField(model_attr='channel')
    channel_exact = indexes.CharField(model_attr='channel', indexed=False)
#    name = indexes.CharField(model_attr='name')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
#    description = indexes.CharField(model_attr='description')
#    keywords = indexes.CharField(model_attr='keywords')
    producers = indexes.MultiValueField()
    producers_exact = indexes.MultiValueField(indexed=False)
    writers = indexes.MultiValueField()
    writers_exact = indexes.MultiValueField(indexed=False)
    reporters = indexes.MultiValueField()
    reporters_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.MultiValueField()
    publication_exact = indexes.MultiValueField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

    def prepare_producers(self, object):
        return [byline.get_full_name() for byline in object.producers.all()]

    def prepare_producers_exact(self, object):
        return [byline.get_full_name() for byline in object.producers.all()]

    def prepare_writers(self, object):
        return [byline.get_full_name() for byline in object.writers.all()]

    def prepare_writers_exact(self, object):
        return [byline.get_full_name() for byline in object.writers.all()]

    def prepare_reporters(self, object):
        return [byline.get_full_name() for byline in object.reporters.all()]
    
    def prepare_reporters_exact(self, object):
        return [byline.get_full_name() for byline in object.reporters.all()]
        
    def prepare_publication(self, object):
        publications = []
        for section in object.channel.section.all():
            publications.append(section.publication.name)
        return publications

    def prepare_publication_exact(self, object):
        publications = []
        for section in object.channel.section.all():
            publications.append(section.publication.name)
        return publications

    def get_updated_field(self):
        return 'last_updated'

    def get_displayed_name(self):
        return 'podcast episode'

    def get_plural_name(self):
        return 'podcast episodes'

    def get_main_result_limit(self):
        return 3

    def get_queryset(self):
        return Episode.objects.filter(pub_date__lte=datetime.datetime.now())

site.register (Episode, EpisodeIndex)
