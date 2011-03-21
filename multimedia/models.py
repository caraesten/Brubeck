# Standard library imports
import os
import urllib
from xml.dom import minidom

# Imports from other dependencies
import gdata.youtube
import gdata.youtube.service
from mutagen.mp3 import MP3

# Imports from Django
from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models

# Imports from Brubeck
from brubeck.core.models import Content
from brubeck.core import imaging

class AttachedFile(Content):
    """Provide support for attaching files to articles."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='%Y/%m%d/attached')
    
    mediatype = 'attached'
    
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return self.file.url
    
    def get_file_extension(self):
        extension = imaging.get_filename_components(self.file)['file_ext']
        return extension[1:]
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'title']

class Video(Content):
    """Provide support for attaching videos to articles.
    
    Some fields in this model might be marked as deprecated. These will be 
    hidden in the admin site.
    
    """
    title = models.CharField(max_length=150, blank=True, db_index=True)
    # FIXME: This was a ForeignKey in the 2008 site. Change this in the 
    # database.
    # FIXME: This had max_length=100 in the 2008 site. Change this in the
    # database.
    url = models.CharField('URL', max_length=255, help_text="This field should contain the URL to view a YouTube or Vimeo video (e.g., http://www.youtube.com/watch?v=n3zX9u0KvB4).")
    # FIXME: This had max_length=100 in the 2008 site. Change this in the
    # database.
    thumbnail = models.CharField(max_length=255, db_index=True, blank=True, help_text="This should contain the URL to a thumbnail image for this video.")
    preview_image = models.ImageField(upload_to='%Y/%m%d/videos', blank=True, null=True, help_text="If you want this video to display a custom image in place of its thumbnail, upload it here.")
    swf = models.CharField(max_length=300, blank=True, help_text="This should contain the URL to a Flash file to embed for this video.")
    description = models.TextField(blank=True, help_text="If this content was provided by a partner news organization (see the \"media partner\" field), be sure to include a link back to the original video.")
    length = models.PositiveSmallIntegerField(blank=True, help_text="Length of the video in seconds.")
    publication = models.ForeignKey('brubeck.publishing.Publication', db_index=True, null=True, help_text="The publication to which this video is linked.")
    tags = models.ManyToManyField('brubeck.tagging.Tag', blank=True, null=True, help_text="Tags that describe this article.")
    webfronts = generic.GenericRelation('brubeck.management.WebFrontItem')
    
    mediatype = 'video'
    
    def __unicode__(self):
        return self.title
    def get_prowl_url(self):
        return '/renters-guide/videos/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    def get_absolute_url(self):
        return '/videos/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    def save(self, *args, **kwargs):
        video_service = None
        if self.url.find('youtube.com') >= 0:
            video_service = 'youtube'
        elif self.url.find('vimeo.com') >= 0:
            video_service = 'vimeo'
        elif self.url.find('blip.tv') >= 0:
            video_service = 'blip'
        
        if video_service == 'youtube':
            video_id = self.url.replace(r'http://www.youtube.com/watch?v=', '')
            
            yt_service = gdata.youtube.service.YouTubeService()
            yt_service.developer_key = settings.YOUTUBE_API_KEY
            yt_service.client_id = settings.YOUTUBE_CLIENT_ID
            
            video_obj = yt_service.GetYouTubeVideoEntry(video_id=video_id)
            
            if not self.title:
                try:
                    self.title = video_obj.media.title.text
                except:
                    pass
            if not self.length:
                try:
                    self.length = video_obj.media.duration.seconds
                except:
                    pass
            if not self.swf:
                try:
                    hd_add = '&fs=1&rel=0&ap=%2526fmt%3D22&hd=1' 
                    swf = '%s%s' % (video_obj.GetSwfUrl(), hd_add)
                    self.swf = swf
                except:
                    pass
            if not self.thumbnail:
                try:
                    self.thumbnail = video_obj.media.thumbnail[1].url
                except:
                    pass
            if not self.description:
                try:
                    self.description = video_obj.media.description.text
                except:
                    pass
        elif video_service == 'vimeo':
            video_id = self.url.replace('http://vimeo.com/', '')
            if video_id == self.url:
                # Nothing's changed. Let's try it with www.
                video_id = self.url.replace('http://www.vimeo.com/', '')
            
            dom = minidom.parse(urllib.urlopen('http://vimeo.com/api/clip/' + video_id + '.xml'))
            
            if not self.title:
                try:
                    self.title = dom.getElementsByTagName('title')[0].firstChild.data
                except:
                    pass
            if not self.length:
                try:
                    self.length = int(dom.getElementsByTagName('duration')[0].firstChild.data)
                except:
                    pass
            if not self.thumbnail:
                try:
                    self.thumbnail = dom.getElementsByTagName('thumbnail_medium')[0].firstChild.data
                except:
                    pass
            if not self.swf:
                self.swf = 'http://vimeo.com/moogaloop.swf?clip_id=' + video_id + '&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1'
            if not self.description:
                try:
                    self.description = dom.getElementsByTagName('caption')[0].firstChild.data
                except:
                    pass
        elif video_service == 'blip':
            api_url = self.url
            if api_url.find('?') >= 0:
                api_url += '&'
            else:
                api_url += '?'
            api_url += 'skin=rss'
            
            dom = minidom.parse(urllib.urlopen(api_url))
            
            if not self.title:
                try:
                    self.title = dom.getElementsByTagName('title')[1].firstChild.data
                except:
                    pass
            if not self.length:
                try:
                    self.length = int(dom.getElementsByTagName('blip:runtime')[0].firstChild.data)
                except:
                    pass
            if not self.swf:
                try:
                    self.swf = dom.getElementsByTagName('blip:embedUrl')[0].firstChild.data
                except:
                    pass
            if not self.thumbnail:
                try:
                    self.thumbnail = dom.getElementsByTagName('blip:smallThumbnail')[0].firstChild.data
                except:
                    pass
            if not self.description:
                try:
                    self.description = dom.getElementsByTagName('blip:puredescription')[0].firstChild.data
                except:
                    pass
        else:
            self.title = "Invalid URL--not a YouTube, Vimeo or blip.tv video"
        super(Video, self).save(*args, **kwargs)
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

from brubeck.core.moderation import AkismetModerator
from brubeck.core.emailing.views import render_email_and_send
from django.contrib.comments.moderation import moderator

class VideoModerator(AkismetModerator):
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
        render_email_and_send(context=context, message_template='multimedia/video_comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True      

moderator.register(Video, VideoModerator)

# NEW: This model includes the following new field: zip
# Be sure to add it to the database.
class Slideshow(Content):
    title = models.CharField(max_length=150, db_index=True)
    # FIXME: This was a ForeignKey in the 2008 site. Change this in the 
    # database.
    description = models.TextField()
    length = models.PositiveSmallIntegerField(help_text="Length of the slideshow in seconds. Enter a zero if there is no audio.")
    image = models.ImageField('preview photo', upload_to='%Y/%m%d/slideshows', help_text="Upload a photo to represent this slideshow on the site. It will automatically be resized for you.")
    swf = models.CharField(max_length=300, blank=True, help_text="URL to the Flash file to embed.")
    zip = models.FileField(upload_to='%Y/%m%d/slideshows', blank=True, null=True, help_text="Upload a zip file containing the slideshow's publish_to_web directory.")
    publication = models.ForeignKey('brubeck.publishing.Publication', db_index=True, null=True, help_text="The publication to which this slideshow is linked.")
    tags = models.ManyToManyField('brubeck.tagging.Tag', blank=True, null=True, help_text="Tags that describe this article.")
    webfronts = generic.GenericRelation('brubeck.management.WebFrontItem')
    
    mediatype = 'slideshow'
    is_horizontal = True
    
    def __unicode__(self):
        return self.title
    def get_prowl_url(self):
        return '/renters-guide/slideshows/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    def get_absolute_url(self):
        return '/slideshows/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        
class SlideshowModerator(AkismetModerator):
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
        render_email_and_send(context=context, message_template='multimedia/slideshow_comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True      

moderator.register(Slideshow, SlideshowModerator)

class AudioClip(Content):
    """
    Provides support for attaching audio files to articles.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    length = models.PositiveSmallIntegerField(blank=True, help_text="This will be automatically determined if you don't specify it. Takes a number of seconds.", null=True)
    audio_file = models.FileField(upload_to='%Y/%m%d/audio', help_text="Only upload MP3 files.")
    image = models.ImageField('preview photo', upload_to='%Y/%m%d/audio', help_text="Upload a photo to represent this clip on the site. It will automatically be resized for you.")
    publication = models.ForeignKey('core.Publication', db_index=True, null=True, help_text="The publication to which this audio clip is linked.")
    tags = models.ManyToManyField('core.Tag', blank=True, null=True, help_text="Tags that describe this article.")
    webfronts = generic.GenericRelation('core.WebFrontItem')
    
    mediatype = 'audioclip'
    
    def __unicode__(self):
        return self.title
    def get_prowl_url(self):
        return '/renters-guide/audio/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    def get_absolute_url(self):
        return '/audio/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)    
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

class AudioClipModerator(AkismetModerator):
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
        render_email_and_send(context=context, message_template='multimedia/audioclip_comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True      

moderator.register(AudioClip, AudioClipModerator)
