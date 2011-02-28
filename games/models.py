# Imports from Django
from django.db import models

# Imports from maneater
from brubeck.core.models import ContentChannel
from brubeck.publishing.models import Issue

# NEW: This is a new model. Be sure to add it to the database.
class GameType(ContentChannel):
    """
    Provides support for multiple games.
    """
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

# NEW: This is a new model. Be sure to add it to the database.
class GameAnswer(models.Model):
    """
    Allows users to publish answers to each game type by uploading PDFs.
    
    Replaces the deprecated, fixed-choice, image-upload model of the 2008 site.
    """
    type = models.ForeignKey(GameType, help_text="For what game type is this answer published?")
    PDF = models.FileField(upload_to='%Y/%m%d/games')
    issue = models.ForeignKey(Issue, help_text="In what issue was this answer published?")
    
    mediatype = 'game_answer'
    
    def __unicode__(self):
        return u'%s %s' % (self.issue.pub_date, self.type)
    
    class Meta:
        ordering = ['issue', 'type']
        unique_together = (('type', 'issue'),)

