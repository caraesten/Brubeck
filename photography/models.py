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

# Imports from maneater
from core.models import Content

# Imports from other sources
from pyPdf import PdfFileReader, PdfFileWriter

class Photo(Content):
    """
    Provides support for photos.
    """
    title = models.CharField(max_length=150, blank=True, null=True, help_text="Optional. Used if this photo will be featured alone on a front page of the site.")
    issue = models.ForeignKey('publishing.Issue', db_index=True, help_text="The issue in which this photo was published.")
    section = models.ForeignKey('publishing.Section', db_index=True)
    mugshot = models.BooleanField(default=False, help_text="Is this photo a mugshot? (This is generally only true if the photo is for a crime story.)")
    illustration = models.BooleanField(default=False, help_text="Is this a photo illustration?")
    image = models.ImageField(upload_to='%Y/%m%d/photos', help_text="Accepts JPEG, GIF or PNG file formats.")
    cutline = models.TextField(blank=True)
    tags = models.ManyToManyField('tagging.Tag', blank=True, null=True, help_text="Tags that describe this photo.")
    
    mediatype = 'photo'
    
    def __unicode__(self):
        """
        Returns the base filename (without directory or extension.
        """
        try:
            return u'%s' % imaging.get_filename_components(self.image)['file_base']
        except:
            return u'Image not found'

    def get_prowl_url(self):
        return '/renters-guide/photos/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)

    def get_absolute_url(self):
        return '/photos/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'section', 'image']
