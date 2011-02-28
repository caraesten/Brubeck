# Imports from standard libraries
from datetime import date

# Imports from Django
from django.db import models
from django.utils.dateformat import format

# Imports from Brubeck
from brubeck.core.models import Content, ContentChannel
from brubeck.core.imaging import get_filename_components
from brubeck.publishing.models import Section
from brubeck.personnel.models import Staffer

class CurrentManager(models.GeoManager):
    """
    Only returns channels that are not considered archived. Handy for listing 
    only current channels.
    """
    def get_query_set(self):
        return super(CurrentManager, self).get_query_set().filter(archived=False)

class ArchivedManager(models.GeoManager):
    """
    Only returns channels that are considered archived. Handy for listing 
    channels no longer published.
    """
    def get_query_set(self):
        return super(ArchivedManager, self).get_query_set().filter(archived=True)

class Channel(ContentChannel):
    """
    Organizes podcast episodes by a common theme. Each channel (front-page
    summary, election specials, etc.) will have its own RSS feed.
    """
    # FIXME: This had unique=True in the 2008 site. Change this in the database.
    section = models.ManyToManyField(Section, db_index=True, blank=True, null=True, help_text="Any sections to which this channel might be related.")
    # FIXME: This had null=True in the 2008 site. Change this in the database.
    keywords = models.CharField(max_length=255, blank=True, help_text="Separated by commas.")
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, help_text="When this channel was last updated. The site will automatically update this field whenever the channel is saved.")
    
    objects = models.GeoManager()
    current = CurrentManager()
    old = ArchivedManager()
    
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return '/podcasts/%s/' % self.slug
    
    class Meta:
        ordering = ['title', 'archived']

class Episode(Content):
    """
    Provides support for individual episodes.
    """
    channel = models.ForeignKey(Channel, db_index=True)
    name = models.CharField('descriptive name', max_length=150, blank=True, help_text="If you want this episode to have an additional title after the channel name and episode number, enter it here.")
    description = models.TextField(help_text="Summarize the episode for a potential listener.")
    keywords = models.CharField(max_length=255, blank=True, help_text="Separated by commas. These will be appended to the channel's list of keywords.")
    file = models.FileField(upload_to='%Y/%m%d/podcasts', help_text="The audio file for this podcast. Please make sure the file is in either MP3 or AAC/MP4 format.")
    
    mediatype = 'podcast'
    
    def __unicode__(self):
        name = u'%s: %s' % (self.channel.title, format(self.pub_date, "N j, Y"))
        if self.name:
            name += u': %s' % self.name
        return name
    def get_absolute_url(self):
        return '/podcasts/episodes/%s/' % self.id
    
    def get_mime_type(self):
        file_ext = get_filename_components(self.file)['file_ext']
        if file_ext == '.m4a':
            return u'audio/aac'
        elif file_ext == '.mp3':
            return u'audio/mpeg'
        else:
            return u'Unknown'
    
    class Meta:
        db_table = 'podcasting_episode'
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'channel', 'name']
        
from brubeck.core.moderation import AkismetModerator
from brubeck.core.emailing.views import render_email_and_send
from django.conf import settings
from django.contrib.comments.moderation import moderator

class EpisodeModerator(AkismetModerator):
    enable_field = 'enable_comments'
    def email(self, comment, content_object, request):
        moderators = []
        chief = settings.EDITORS['chief']
        moderators.append(chief)
        managing = settings.EDITORS['managing']
        moderators.append(managing)
        online_dev = settings.EDITORS['online_dev']
        moderators.append(online_dev)
        multimedia = settings.EDITORS['multimedia']
        moderators.append(multimedia)
        online_assistant = settings.EDITORS['online_assistant']
        moderators.append(online_assistant)        
        context = {'comment': comment, 'content_object': content_object}
        subject = 'New comment awaiting moderation on "%s"' % content_object
        render_email_and_send(context=context, message_template='podcasts/comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True

moderator.register(Episode, EpisodeModerator)
