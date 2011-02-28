# Imports from Django
from django.contrib.gis.db import models

# Imports from Brubeck
from brubeck.core.models import Content, ContentChannel
from brubeck.personnel.models import Staffer
from brubeck.publishing.models import Issue, Section, Volume

# NEW: This model contains the following new field: active
# Be sure to add it to the database.
class ComicStrip(ContentChannel):
    """
    Provide support for multiple strips.
    
    Some fields in this model might be marked as deprecated. These will be 
    hidden in the admin site.
    """
    volume = models.ForeignKey(Volume, db_index=True, blank=True, null=True, help_text="The volume of The Maneater in which this comic strip appears.")

    objects = models.GeoManager()
    
    def __unicode__(self):
        if self.volume:
            return u'%s (Volume %s)' % (self.name, self.volume.volume_id)
        else:
            return self.name
    def get_absolute_url(self):
        return '/comics/%s/' % self.slug
    
    class Meta:
        ordering = ['name']

class ComicEpisode(Content):
    """
    Provide support for publishing episodes of strips.
    """
    issue = models.ForeignKey(Issue, db_index=True, help_text="The issue in which this episode was published.")
    strip = models.ForeignKey(ComicStrip)
    image = models.ImageField(upload_to='%Y/%m%d/comics')
    
    mediatype = 'comic'
    is_horizontal = True

    objects = models.GeoManager()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.strip.title, self.pub_date)
    def get_absolute_url(self):
        return '/comics/%s/%s/%s/%s/%s/' % (self.strip.slug, self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

class EditorialCartoon(Content):
    """Provide support for editorial cartoons."""
    issue = models.ForeignKey(Issue, db_index=True, help_text="The issue in which this editorial cartoon was published.")
    section = models.ForeignKey(Section, db_index=True)
    image = models.ImageField(upload_to='%Y/%m%d/graphics', help_text="Accepts JPEG, GIF or PNG file formats.")
        
    mediatype = 'editorialcartoon' 
        
    def __unicode__(self):
        """Returns the base filename (without directory or extension."""
        return u'%s' % imaging.get_filename_components(self.image)['file_base']
        
    def get_absolute_url(self):
        return '/editorial-cartoons/%s/%s/%s/%s/' % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.id)
        
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date', 'section']
