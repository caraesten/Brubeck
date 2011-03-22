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
from brubeck.core.models import Content
from brubeck.publishing.models import Issue, Section
from brubeck.events.models import Calendar, Event
from brubeck.articles.models import PublishedManager

# Imports from other sources
# from positions.fields import PositionField
from pyPdf import PdfFileReader, PdfFileWriter

# This is a hippopotamus.
#   .-''''-. _    
#  ('    '  '0)-/)
#  '..____..:    \._
#    \u  u (        '-..------._
#    |     /      :   '.        '--.
#   .nn_nn/ (      :   '            '\
#  ( '' '' /      ;     .             \
#   ''----' "\          :            : '.
#          .'/                           '.
#         / /                             '.
#        /_|       )                     .\|
#          |      /\                     . '
#          '--.__|  '--._  ,            /
#                       /'-,          .'
#                      /   |        _.' 
#                     (____\       /    
#                           \      \    
#                            '-'-'-'    

class NewsBurst(models.Model):
    """
    Provides support for posting brief updates on breaking news.
    
    Generally will show up on the front page only.
    """
    title = models.CharField(max_length=150, db_index=True)
    pub_date = models.DateTimeField('date published')
    published = models.BooleanField()
    body = models.TextField(blank=True)
    link = models.CharField(max_length=200, blank=True)
    
    mediatype = 'newsburst'
    
    # Managers--both the default (normal behavior) and one that just returns
    # published news bursts.
    objects = models.GeoManager()
    get_published = PublishedManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

# NEW: This is a new model. Be sure to add it to the database.
class WebFront(models.Model):
    MULTIMEDIA_CHOICES = (
        ('normal', "None--just normal articles"),
        ('video', "Video"),
        ('slideshow', "Slideshow"),
        ('custom', "Custom content"),
    )
    WEBFRONT_TYPE_CHOICES = (
        ('site', "Website front page"),
        ('section', "Section front page"),
        ('special', "Special section front page"),
    )
    TWO_WEEKS_AGO = date.today() - timedelta(14)
    site = models.ForeignKey(Site, help_text="Which site should use this front page?")
    type = models.CharField(max_length=10, choices=WEBFRONT_TYPE_CHOICES, default='site', help_text="Is this the front page of one of our websites, the front of a section or the front of a special section?")
    issue = models.ForeignKey(Issue, help_text="Which issue (along with any subsequent online updates) should the site use to generate its front page?")
    top_sections = models.ManyToManyField(Section, help_text="Which sections should be displayed \"above the fold,\" so to speak--or at the top of the site, immediately below the navigation bar? Please choose an <strong>odd</strong> number of sections for The Maneater (five is ideal).")
    show_multimedia = models.CharField(max_length=10, choices=MULTIMEDIA_CHOICES, blank=True, help_text="Should the front page display some sort of centerpiece content that isn't a normal article? (If this is set, one of the entries in \"Top sections\" above (specifically, the one with the fewest stories) will be ignored to make room.)")
    show_election_front = models.BooleanField(help_text="Should the site display a large panel of our election coverage above all other content (with the exception of a live stream, if enabled)? <strong>Be sure to set up an election front before checking this box.</strong> (If you don't, nothing's going to break, but you might end up being a little embarrassed when you're showing the world the information from the previous election.)")
    other_info = models.TextField(blank=True, help_text="Is there anything else that should be displayed on the front page? (Such content is <em>rare</em> and is usually an announcement, such as the one every semester inviting people to apply for editorial positions.)")
    calendar = models.ForeignKey(Calendar, help_text="From which calendar should the front show a list of upcoming events?")
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    def __unicode__(self):
        return repr(self.issue)
    
    class Meta:
        get_latest_by = 'last_updated'
        ordering = ['-id']
        verbose_name = 'Web front'
        
class WebFrontItem(models.Model):
    webfront = models.ForeignKey(WebFront, related_name='item_set')
    priority = models.PositiveSmallIntegerField()
    object = models.ForeignKey(Content)

    def __unicode__(self):
        return "Object #%s for WebFront %s" % (self.priority, self.webfront)

    class Meta:
        ordering = ['priority']
        verbose_name = 'Web front item'

class CustomCenterpiece(Content):
    title = models.CharField(max_length=300)
    link = models.CharField('URL', max_length=300, blank=True, null=True, help_text="Optional. To what URL should the custom centerpiece headline link?")
    image = models.ImageField(upload_to='%Y/%m%d/customfronts')
    description = models.TextField()

    mediatype = 'custom'

    def __unicode__(self):
        return self.title

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        verbose_name = 'Custom centerpiece'
