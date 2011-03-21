# Allow the use of / operator for division to yield floats instead of integers:
# http://docs.python.org/whatsnew/2.2.html#pep-238-changing-the-division-operator
from __future__ import division

# Imports from standard libraries
from datetime import date, timedelta
import hashlib
import os
import urllib2

# Imports from Django
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.markup.templatetags.markup import markdown
from django.contrib.sites.models import Site
from django.core.files import File
from django.contrib.gis.db import models
from django.utils import simplejson

# Imports from Brubeck
from brubeck.core import imaging
from brubeck.core.models import Content
from brubeck.publishing.models import Issue, Section
from brubeck.articles.models import Article
from brubeck.photography.models import Photo

# Imports from other sources
# from positions.fields import PositionField
from pyPdf import PdfFileReader, PdfFileWriter

class Graphic(Content):
    """Provide support for graphics (any art that isn't a photo)."""
    issue = models.ForeignKey(Issue, db_index=True, help_text="The issue in which this graphic was published.")
    section = models.ForeignKey(Section, db_index=True)
    image = models.ImageField(upload_to='%Y/%m%d/graphics', help_text="Accepts JPEG, GIF or PNG file formats.")
    
    mediatype = 'graphic'

    objects = models.GeoManager()
    
    def __unicode__(self):
        """Returns the base filename (without directory or extension."""
        return u'%s' % imaging.get_filename_components(self.image)['file_base']

    def get_prowl_url(self):
        return '/renters-guide/graphics/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)

    def get_absolute_url(self):
        return '/graphics/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'section']

class Layout(Content):
    """
    Provides support for layout PDFs.
    """
    TYPE_CHOICES = (
        ('ad', "Ad Full"),
        ('cover', "Issue Front Cover"),
        ('feat', "Feature Page"),
        ('page', "Regular Page"),
        ('spec', "Special section"),
    )
    TWO_WEEKS_AGO = date.today() - timedelta(14)
    issue = models.ForeignKey(Issue, db_index=True, help_text="The issue in which this layout was published.")
    section = models.ForeignKey(Section, db_index=True,help_text="The Maneater's cover should go in News. MOVE's cover should go in MOVE Features.")
    first_page = models.PositiveIntegerField(db_index=True, db_column='firstpage', help_text="For single-page layouts, the page number. For multi-page PDFs, the first page number represented by this layout.")
    last_page = models.PositiveIntegerField(db_index=True, blank=True, null=True, db_column='lastpage', help_text="For single-page layouts, <strong>leave this blank</strong>. For multi-page layouts, the last page number represented by this PDFs.")
    type = models.CharField(max_length=5, db_index=True, choices=TYPE_CHOICES, default='cover')
    title = models.CharField(max_length=150, blank=True, help_text="Put the main headline or title here. Please leave this blank if this page is the cover.")
    thumbnail = models.ImageField(upload_to='%Y/%m%d/pages/thumbs', blank=True, null=True, help_text="Deprecated. Has been replaced with the same thumbnail system as core.SpecialSection, core.Photo and core.Graphic.")
    PDF = models.FileField(upload_to='%Y/%m%d/pages')
    articles = models.ManyToManyField(Article, db_index=True, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, related_name='contents_articles', blank=True, null=True, help_text="Articles shown on this layout.")
    photos = models.ManyToManyField(Photo, db_index=True, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Photos shown on this layout.")
    graphics = models.ManyToManyField(Graphic, db_index=True, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Graphics shown on this layout.")

    mediatype = 'layout'

    objects = models.GeoManager()
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            if self.first_page == 1:
                return u'Front page'
            elif self.last_page:
                return u'Pages %s - %s' % (self.first_page, self.last_page)
            else:
                return u'Page %s' % self.first_page
    def get_absolute_url(self):
        return '/layouts/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'first_page', 'last_page']
        unique_together = (('issue', 'first_page', 'last_page'),)
