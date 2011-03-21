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

# Imports from other source
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

class PublishedManager(models.Manager):
    """
    Only returns articles that have been marked as published. This is handy for
    such content as articles and blog posts that might need editing before being
    published.
    """
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(is_published=True)

class Article(Content):
    """
    Provides support for news stories. The workhorse of the site.
    
    Some fields in this model might be marked as deprecated. These will be
    hidden in the admin site.
    """
    TWO_WEEKS_AGO = date.today() - timedelta(14)
    TYPE_CHOICES = (
        ('story', "Story/Brief"),
        # ('online', "Online Exclusive"),
        ('online', "Web Update"),
        ('column', "Column"),
        ('editorial', "Editorial"),
        ('letter', "Letter to the Editor"),
        ('guest', "Guest Column"),
    )
    title = models.CharField(max_length=150, db_index=True)
    issue = models.ForeignKey('brubeck.publishing.Issue', db_index=True, help_text="The issue in which this article was published.")
    section = models.ForeignKey('brubeck.publishing.Section', db_index=True)
    layout = models.ForeignKey('brubeck.design.Layout', db_index=True, blank=True, null=True, db_column='page_id', help_text="Deprecated. In the 2008 site, this held the relation between Layout and Article objects. This relation is now in Layout.articles as a ManyToManyField.")
    type = models.CharField(max_length=30, db_index=True, choices=TYPE_CHOICES, default='story')
    priority = models.PositiveIntegerField('priority/page number', db_index=True, default=10, help_text="The lower this number, the higher the article is displayed (compared to other articles published the same day). <strong>You should use the page number for this</strong>, but it isn't strictly required that you do so.<br />If you set this to 0 (the number zero), it will become the top story on the site and be automatically sent out over Twitter.")
    updated = models.BooleanField(db_index=True, default=False, help_text="Whether or not this article has been updated since it was last posted. If this is checked, the article will show the date and time when it was most recently saved on the front page, the archives and the article page itself.")
    cdeck = models.CharField('c-deck', max_length=255, blank=True, help_text="The optional text that appears before the article. If provided, this becomes the article's teaser in various places on the site.")
    body = models.TextField(help_text="The content of the article. Accepts HTML (for embeds and such), but primarily uses <a href=\"http://daringfireball.net/projects/markdown/basics\">Markdown</a> formatting. The basics:<ul><li>Separate paragraphs by blank lines.</li><li>Italicize words _like this_.</li><li>Make words (including subheads) bold **like this**.</li><li>Link things like so: Go to [themaneater.com](http://www.themaneater.com/).</li></ul>")
    photos = models.ManyToManyField('brubeck.photography.Photo', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Photos attached to this article. (Can select photos published within the last two weeks.)")
    editorial_cartoons = models.ManyToManyField('brubeck.comics.EditorialCartoon', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Editorial cartoons attached to this article. (You can select cartoons published within the last two weeks.)")
    graphics = models.ManyToManyField('brubeck.design.Graphic', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Graphics attached to this article. (Can select graphics published within the last two weeks.)")
    attached_files = models.ManyToManyField('brubeck.multimedia.AttachedFile', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Other files attached to this article. (Can select files uploaded within the last two weeks.)")
    videos = models.ManyToManyField('brubeck.multimedia.Video', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Videos attached to this article. (Can select videos published within the last two weeks.)")
    slideshows = models.ManyToManyField('brubeck.multimedia.Slideshow', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Slideshows attached to this article. (Can select slideshows published within the last two weeks.)")
    audio_clips = models.ManyToManyField('brubeck.multimedia.AudioClip', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Audio clips attached to this article. (Can select audio clips published within the last two weeks.)")
    podcast_episodes = models.ManyToManyField('brubeck.podcasts.Episode', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Podcast episodes related to this article. (Can select podcast episodes published in the last two weeks.)")
    tags = models.ManyToManyField('brubeck.tagging.Tag', blank=True, null=True, help_text="Tags that describe this article.")
    calendar = models.ForeignKey('brubeck.events.Calendar', blank=True, null=True, help_text="If we've created a calendar that has to do with the content of this article, select it here.")
    map = models.ForeignKey('brubeck.mapping.Map', verbose_name='attached map', blank=True, null=True, help_text="Choose a map to display with this article.")
    polls = models.ManyToManyField('brubeck.voxpopuli.Poll', limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, verbose_name='attached polls', blank=True, null=True, help_text="Choose a poll to display with this article.")
    slug = models.SlugField(db_index=True, unique_for_date='pub_date', help_text="Used for URLs. <strong>DO NOT ENTER THE RUNSHEET SLUG.</strong>. Autogenerated from title.")
    blurb = models.TextField(blank=True, help_text="Use this if you would like the top story to show something other than its first 40 words on the front page, or if you would like a story other than the top one to show something other than its c-deck in the archives.")
    sidebar = models.TextField(blank=True, help_text="Use this if you'd like for specific sidebar content (movie review information, related links, etc.) to show up with the article.")
    runsheet_slug = models.CharField(max_length=50, blank=True, null=True, help_text="The brief phrase used to describe this article on the runsheet. Helps to ensure articles are given the same priority online and in print.")
    teaser_photo = models.ImageField(upload_to='%Y/%m%d/articles/teaser-photos', blank=True, null=True, help_text="If this article has a magazine-style illustration (for use with top stories on MOVE and Columbia Prowl), upload it here.")
    webfronts = generic.GenericRelation('brubeck.management.WebFrontItem')
    
    mediatype = 'article'
    
    # Managers--both the default (normal behavior) and one that just returns
    # published articles.
    objects = models.GeoManager()
    get_published = PublishedManager()
    
    def __unicode__(self):
        return self.title
    def save(self, *args, **kwargs):
        # FIXME: Look into ping_google and how it was used before.
        try:
            if self.body.count('\r\n\r\n') or self.body.count('\n\n'):
                pass
            else:
                self.body = self.body.replace('\r', '')
                self.body = self.body.replace('\n', '\r\n\r\n')
        except:
            pass
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.section.publication.name == 'Columbia Prowl':
            return 'http://%s/renters-guide/stories/%s/%s/%s/%s/' % (self.section.publication.site.domain, self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)
        else:
            return 'http://%s/stories/%s/%s/%s/%s/' % (self.section.publication.site.domain, self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)
            
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['issue', '-pub_date', 'priority', 'section', 'title']
            
from brubeck.core.moderation import AkismetModerator
from brubeck.core.emailing.views import render_email_and_send
from django.conf import settings
from django.contrib.comments.moderation import moderator

class ArticleModerator(AkismetModerator):
    enable_field = 'enable_comments'
    def email(self, comment, content_object, request):
        moderators = []
        chief = settings.EDITORS['chief']
        moderators.append(chief)
        managing = settings.EDITORS['managing']
        moderators.append(managing)
        online_dev = settings.EDITORS['online_dev']
        moderators.append(online_dev)
        context = {'comment': comment, 'content_object': content_object}
        subject = 'New comment awaiting moderation on "%s"' % content_object
        render_email_and_send(context=context, message_template='core/comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True      

moderator.register(Article, ArticleModerator)
    
    
class Correction(models.Model):
    """
    Provides support for publishing corrections to articles.
    
    This model is edited inline as part of the Article change page.
    """
    article = models.ForeignKey(Article)
    date_corrected = models.DateTimeField()
    correction = models.CharField(max_length=500)
    
    def __unicode__(self):
        return "Correction to %s" % self.article
    
    class Meta:
        get_latest_by = 'date_corrected'
        ordering = ['-date_corrected', 'article']
