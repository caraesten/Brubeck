import datetime
from haystack import indexes
from haystack.sites import site
from brubeck.multimedia.models import AudioClip, Slideshow, Video

class AudioClipIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
#    description = indexes.CharField(model_attr='description')
#    static_byline_producer = indexes.CharField(model_attr='static_byline_producer', null=True)
#    static_byline_reporter = indexes.CharField(model_attr='static_byline', null=True)
    producers = indexes.MultiValueField()
    producers_exact = indexes.MultiValueField(indexed=False)
    reporters = indexes.MultiValueField()
    reporters_exact = indexes.MultiValueField(indexed=False)
    tags = indexes.MultiValueField()
    tags_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

    def prepare_producers(self, obj):
        return [byline.get_full_name() for byline in obj.producers.all()]

    def prepare_producers_exact(self, obj):
        return [byline.get_full_name() for byline in obj.producers.all()]

    def prepare_reporters(self, obj):
        return [byline.get_full_name() for byline in obj.reporters.all()]

    def prepare_reporters_exact(self, obj):
        return [byline.get_full_name() for byline in obj.reporters.all()]

    def prepare_tags(self, obj):
        return [tag.title for tag in obj.tags.all()]
        
    def prepare_tags_exact(self, obj):
        return [tag.title for tag in obj.tags.all()]
    
    def prepare_publication(self, object):
        return object.publication.name
        
    def prepare_publication_exact(self, object):
        return object.publication.name

    def get_updated_field(self):
        return 'last_updated'

    def get_queryset(self):
        return AudioClip.objects.filter(pub_date__lte=datetime.datetime.now())

site.register (AudioClip, AudioClipIndex)

class SlideshowIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
#    description = indexes.CharField(model_attr='description')
#    static_byline = indexes.CharField(model_attr='static_byline')
    contributors = indexes.MultiValueField()
    contributors_exact = indexes.MultiValueField(indexed=False)
    tags = indexes.MultiValueField()
    tags_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

    def prepare_contributors(self, object):
        return [byline.get_full_name() for byline in object.byline.all()]

    def prepare_contributors_exact(self, object):
        return [byline.get_full_name() for byline in object.byline.all()]

    def prepare_tags(self, object):
        return [tag.title for tag in object.tags.all()]
    
    def prepare_tags_exact(self, object):
        return [tag.title for tag in object.tags.all()]

    def prepare_publication(self, object):
        try:
            return object.publication.name
        except:
            pass
        
    def prepare_publication_exact(self, object):
        try:
            return object.publication.name
        except:
            pass
    
    def get_updated_field(self):
        return 'last_updated'

    def get_queryset(self):
        return Slideshow.objects.filter(pub_date__lte=datetime.datetime.now())

site.register (Slideshow, SlideshowIndex)

class VideoIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
#    description = indexes.CharField(model_attr='description')
#    static_byline = indexes.CharField(model_attr='static_byline')
    authors = indexes.MultiValueField()
    authors_exact = indexes.MultiValueField(indexed=False)
    tags = indexes.MultiValueField()
    tags_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

    def prepare_authors(self, object):
        return [byline.get_full_name() for byline in object.byline.all()]
        
    def prepare_authors_exact(self, object):
        return [byline.get_full_name() for byline in object.byline.all()]

    def prepare_tags(self, object):
        return [tag.title for tag in object.tags.all()]

    def prepare_tags_exact(self, object):
        return [tag.title for tag in object.tags.all()]

    def prepare_publication(self, object):
        return object.publication.name
        
    def prepare_publication_exact(self, object):
        return object.publication.name
    
    def get_updated_field(self):
        return 'last_updated'

    def get_queryset(self):
        return Video.objects.filter(pub_date__lte=datetime.datetime.now())

site.register (Video, VideoIndex)
