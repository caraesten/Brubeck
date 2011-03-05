
import datetime
from haystack import indexes
from haystack.sites import site
from brubeck.blogs.models import Entry, Blog

class EntryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    blog = indexes.CharField(model_attr='blog')
    blog_exact = indexes.CharField(model_attr='blog', indexed=False)
    byline = indexes.CharField(null=True)
    byline_exact = indexes.CharField(null=True, indexed=False)
    static_byline = indexes.CharField(model_attr='blog', null=True)
#    body = indexes.CharField(model_attr='body')
    tags = indexes.MultiValueField()
    tags_exact = indexes.MultiValueField(indexed=False)
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

    def prepare_tags(self, object):
        return [tag.title for tag in object.tags.all()]
        
    def prepare_tags_exact(self, object):
        return [tag.title for tag in object.tags.all()]

    def	prepare_byline(self, obj):
        try:
       	    return "%s %s" % (obj.byline.first_name, obj.byline.last_name)
        except:
            return None

    def	prepare_byline_exact(self, obj):
        try:
       	    return "%s %s" % (obj.byline.first_name, obj.byline.last_name)
        except:
            return None
    
    def prepare_publication(self, object):
        return object.blog.section.publication.name
        
    def prepare_publication_exact(self, object):
        return object.blog.section.publication.name

    def get_updated_field(self):
        return 'last_updated'

    def get_queryset(self):
        return Entry.objects.filter(pub_date__lte=datetime.datetime.now())

site.register (Entry, EntryIndex)

class BlogIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    title = indexes.CharField(model_attr='title')
#    description = indexes.CharField(model_attr='description')
    section = indexes.CharField(model_attr='section')
    section_exact = indexes.CharField(model_attr='section', indexed=False)
    publication = indexes.CharField()
    publication_exact = indexes.CharField(indexed=False)

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(BlogIndex, self).prepare(object)
#        return self.prepared_data

    def prepare_publication(self, object):
        return object.section.publication.name
        
    def prepare_publication_exact(self, object):
        return object.section.publication.name

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Blog.objects.all()
        
site.register (Blog, BlogIndex)
