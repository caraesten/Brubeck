# Imports from Django.
from django.contrib.sites.models import Site
from django.db import models

# Imports from other dependencies. For now, Grappelli's 'PositionField.'
# from positions.fields import PositionField

# Imports from Brubeck.
from brubeck.core.models import Category, ContentChannel, Content
from brubeck.personnel.models import Staffer
from brubeck.publishing.models import Publication, Volume
from brubeck.tagging.models import Tag

# Create your models here.

class BookType(Category):

    def __unicode__(self):
        return self.name

class Book(ContentChannel):
    contributors = models.ManyToManyField(Staffer)
    introductory_message = models.TextField(blank=True, null=True)
    is_update = models.BooleanField()
    pdf = models.FileField(upload_to='manuals/%Y-%m', blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True)
    publication = models.ManyToManyField(Publication, null=True)
    site = models.ManyToManyField(Site, null=True)
    type = models.ForeignKey(BookType)
    volume = models.ManyToManyField(Volume, null=True)

    def __unicode__(self):
        return self.name

class Entry(models.Model):
    book = models.ManyToManyField(Book)
    justification = models.TextField(blank=True, null=True)
###    mistaken_values = models.TextField()
    order_by = models.CharField(max_length=1)
    slug = models.SlugField()
    tags = models.ManyToManyField(Tag, blank=True, null=True, related_name='docs_entry_set')
    text = models.TextField()
    title = models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title

class Example(models.Model):
    EXAMPLE_CHOICES = (
        ('P', 'Preferred usage'),
        ('A', 'Accepted (not preferred) usage'),
        ('I', 'Incorrect usage')
    )
    entry = models.ForeignKey(Entry)
    explanation = models.CharField(max_length=400)
    priority = models.SmallIntegerField()
    type = models.CharField(max_length=1, choices=EXAMPLE_CHOICES)
    usage = models.CharField(max_length=400)

    def __unicode__(self):
        return '%s %s' % (self.entry, self.get_type_display())
