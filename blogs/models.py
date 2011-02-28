# Imports from standard libraries
from datetime import date, datetime, timedelta

# Imports from other dependencies
from akismet import Akismet
# from comment_utils.managers import CommentedObjectManager
# from comment_utils.moderation import CommentModerator, moderator

# Imports from Django
from django.conf import settings
from django.contrib.comments.signals import comment_was_posted, comment_will_be_posted
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.contrib.gis.db import models
from django.template import Context, loader
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str

# Imports from Brubeck
from brubeck.core.models import Content, ContentChannel
from brubeck.personnel.models import Position, Staffer
from brubeck.photography.models import Photo
from brubeck.tagging.models import Tag
from brubeck.publishing.models import Section
from brubeck.core.emailing.views import render_email_and_send
from brubeck.multimedia.models import AttachedFile, AudioClip, Slideshow, Video

class CurrentManager(models.Manager):
    """
    Only returns non-live blogs that are not considered archived. Handy for 
    listing only current blogs.
    """
    def get_query_set(self):
        return super(CurrentManager, self).get_query_set().filter(is_live_blog=False).filter(archived=False)

class ArchivedManager(models.Manager):
    """
    Only returns non-live blogs that are considered archived. Handy for listing 
    blogs no longer published.
    """
    def get_query_set(self):
        return super(ArchivedManager, self).get_query_set().filter(archived=True)

class LiveBlogManager(models.Manager):
    """
    Only returns live blogs.
    """
    def get_query_set(self):
        TWENTY_FOUR_HOURS_AGO = datetime.now() - timedelta(hours=24)
        return super(LiveBlogManager, self).get_query_set().filter(is_live_blog=True)

class ActiveLiveBlogManager(models.Manager):
    """
    Only returns live blogs active within the past 24 hours. (Keeps us from
    cluttering up the blog index.)
    """
    def get_query_set(self):
        TWENTY_FOUR_HOURS_AGO = datetime.now() - timedelta(hours=24)
        return super(ActiveLiveBlogManager, self).get_query_set().filter(is_live_blog=True).filter(entry__pub_date__gte=TWENTY_FOUR_HOURS_AGO).distinct()

class Blog(ContentChannel):
    """
    Organizes entries into separate blogs.
    """
    section = models.ForeignKey(Section, db_index=True)
    # Change these in the database.
    editorial_moderators = models.ManyToManyField(EditorPosition, db_index=True, blank=True, null=True, help_text="Select the positions of editors who will moderate comments for this blog.")
    staff_moderators = models.ManyToManyField(Staffer, db_index=True, blank=True, null=True, limit_choices_to={'is_active': True}, help_text="Select any additional Maneater staffers who will moderate comments for this blog.")
    moderators = models.CharField(max_length=150, blank=True, help_text="Enter the e-mail addresses of anyone else who will moderate comments for this blog. Separate them with commas.")
    is_live_blog = models.BooleanField('is live blog?', default=False, db_index=True, help_text="Is this blog going to be used for a short period of time to cover a specific event? <strong>Note:</strong> This setting does not determine whether a blog is still active, so archived live blogs should still have this box checked.")
    objects = models.GeoManager()
    current = CurrentManager()
    old = ArchivedManager()
    live_blogs = LiveBlogManager()
    active_live_blogs = ActiveLiveBlogManager()
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True, help_text="When this blog was last updated. The site will automatically update this field whenever the blog is saved.")

    
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        """
        Adds today's date to the slug of a new live blog to avoid collisions.
        """
        if self.is_live_blog:
            date_slug = slugify(date.today().strftime('%Y %b %d'))
            self.slug = self.slug[:38]
            self.slug = '%s-%s' % (self.slug, date_slug)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/blogs/%s/' % self.slug
    
    class Meta:
        ordering = ['name']

class PublishedManager(models.Manager):
    """
    Only returns entries that have been marked as published. This is handy for
    such content as articles and blog posts that might need editing before being
    published.
    """
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published=True)

# NEW: This model contains the following new fields: enable_comments, published,
# tags
# Be sure to add them to the database.
class Entry(Content):
    """
    Allows users to post individual blog entries.
    """
    TWO_WEEKS_AGO = date.today() - timedelta(14)
    title = models.CharField(max_length=100)
    blog = models.ForeignKey(Blog)
    body = models.TextField(help_text="The content of the entry. Accepts HTML (for embeds and such), but primarily uses <a href=\"http://daringfireball.net/projects/markdown/basics\">Markdown</a> formatting. The basics:<ul><li>Separate paragraphs by blank lines.</li><li>Italicize words _like this_.</li><li>Make words (including subheads) bold **like this**.</li><li>Link things like so: Go to [themaneater.com](http://www.themaneater.com/).</li></ul>")
    photos = models.ManyToManyField(Photo, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Photos attached to this article. (Can select photos published within the last two weeks.)")
    # photos = models.ManyToManyField(Photo, blank=True, null=True, help_text="Photos attached to this article. (Can select photos published within the last two weeks.)")
    attached_files = models.ManyToManyField(AttachedFile, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Other files attached to this entry. (Can select files uploaded within the last two weeks.)")
    videos = models.ManyToManyField(Video, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Videos attached to this entry. (Can select videos published within the last two weeks.)")
    slideshows = models.ManyToManyField(Slideshow, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Slideshows attached to this entry. (Can select slideshows published within the last two weeks.)")
    audio_clips = models.ManyToManyField(AudioClip, limit_choices_to={'pub_date__gte': TWO_WEEKS_AGO}, blank=True, null=True, help_text="Audio clips attached to this entry. (Can select audio clips published within the last two weeks.)")
    tags = models.ManyToManyField(Tag, blank=True, null=True, help_text="Tags that describe this entry.")
    slug = models.SlugField(unique_for_date='pub_date', help_text="Used for URLs. Autogenerated from title.")

    mediatype = 'blog'
    
    # Managers--both the default (normal behavior) and one that just returns
    # published entries.
    objects = models.GeoManager()
    get_published = PublishedManager()
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return 'http://%s/blogs/%s/%s/%s/%s/%s/' % (self.blog.section.publication.site.domain, self.blog.slug, self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)
        
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'blog']
        verbose_name_plural = "entries"

from brubeck.core.moderation import AkismetModerator
from django.contrib.comments.moderation import moderator
    
class EntryModerator(AkismetModerator):
    enable_field = 'enable_comments'
    def email(self, comment, content_object, request):
        content_object = comment.content_object
        if content_object.blog.editorial_moderators:
            editorial_moderators = content_object.blog.editorial_moderators
            editor_emails = []
            for editor in editorial_moderators.all():
                eds = editor.tenure_set.filter(current=True)
                for ed in eds.all():
                    if ed.editor.email:
                        editor_emails.append(ed.editor.email)
        if content_object.blog.staff_moderators:
            staff_moderators = content_object.blog.staff_moderators
            staff_emails = []
            for staffer in staff_moderators.all():
                staff_emails.append(staffer.email)
        moderators = content_object.blog.moderators
        moderators = moderators.split(',')
        for each_moderator in moderators:
            each_moderator = each_moderator.strip()
        moderators.extend(staff_emails)
        moderators.extend(editor_emails)
        context = {'comment': comment, 'content_object': content_object}
        subject = 'New comment awaiting moderation on "%s"' % content_object
        render_email_and_send(context=context, message_template='blogs/comment_notification_email.txt', subject=subject, recipients=moderators)
    def moderate(self, comment, content_object, request):
        return True

moderator.register(Entry, EntryModerator)
