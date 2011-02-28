# Allow the use of / operator for division to yield floats instead of integers:
# http://docs.python.org/whatsnew/2.2.html#pep-238-changing-the-division-operator
from __future__ import division

# Imports from standard libraries
from datetime import date, timedelta
import hashlib
import os
import simplejson
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

# Imports from other sources
from positions.fields import PositionField
from pyPdf import PdfFileReader, PdfFileWriter

class Publication(models.Model):
    """
    Provides support for multiple publications.
    
    A publication may be identified either by its name (guaranteed to be unique
    at the database level) or its associated Site (part of 
    django.contrib.sites). Views will probably use the latter more often.
    """
    name = models.CharField(max_length=50, db_index=True, unique=True)
    description = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return u'http://%s/' % self.site.domain
    
    class Meta:
        ordering = ['name']

class Section(ContentChannel):
    """
    Provides support for organizing content by section.
    """
    publication = models.ForeignKey(Publication, db_index=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.publication, self.name)
    def get_absolute_url(self):
        return '/section/%s/' % self.slug
    
    class Meta:
        ordering = ['publication', 'name']
        unique_together = (('name', 'publication'), ('slug', 'publication'))

class Volume(models.Model):
    """
    Provides support for individual volumes.
    """
    volume_id = models.PositiveIntegerField('volume number', db_index=True)
    first_issue = models.DateField(help_text="When was the first issue of this volume published?")
    description = models.CharField("time period", max_length=100, help_text="i.e., <em>Spring 2008</em> or <em>Fall 2007 - Spring 2008</em>")
    publication = models.ForeignKey(Publication, db_index=True)
    
    def __unicode__(self):
        return u'%s v. %s' % (self.publication, self.volume_id)
    
    class Meta:
        get_latest_by = 'first_issue'
        ordering = ['-first_issue', 'publication', 'volume_id']
        unique_together = (('volume_id', 'publication'), ('first_issue', 'publication'))

class Issue(models.Model):
    """
    Provides support for grouping content by issue.
    
    Some fields in this model might be marked as deprecated. These will be 
    hidden in the admin site.
    """
    volume = models.ForeignKey(Volume, db_index=True)
    issue_id = models.PositiveIntegerField('issue number', db_index=True, blank=True, null=True, help_text="Fill this in unless this is an online update set.")
    pub_date = models.DateTimeField(db_column='date', help_text="When was this issue published?")
    online_update = models.BooleanField(default=False, help_text="Is this actually a set of online updates instead of an issue?")
    old_archive = models.BooleanField(default=False, help_text="Is this an imported set of articles from the old (PHP) site? (Should never be checked for new issues.)")
    # FIXME: This had null=True in the 2008 site. Change this in the database.
    name = models.CharField(max_length=50, blank=True, help_text="Deprecated. Was used to collect articles for special events before we had blogs.")
    poll = models.ForeignKey('brubeck.voxpopuli.Poll', db_index=True, blank=True, null=True, help_text="Deprecated. Was once used to publish polls on the front page.")
    streaming = models.BooleanField("show streaming video?", default=False, help_text="Deprecated. Was used to show live video streams on the front page.")
    color = models.CharField("primary website color", max_length=6, blank=True, null=True, help_text="Enter the six-characted hex code of the color you want featured on the site (note: this is a MOVE-specific feature).")
    masthead_image = models.ImageField('MOVE masthead image', upload_to='style/%Y-%m/images/masthead/', blank=True, null=True, help_text='If an image is uploaded here, it will replace the standard masthead on the MOVE site.')
    maneater_masthead_image = models.ImageField(upload_to='style/%Y-%m/images/masthead/', blank=True, null=True, help_text='If an image is uploaded here, it will replace the standard masthead on themaneater.com.')
    render_issue_pdf = models.BooleanField('Create issue PDF', default=False, help_text='If you check this box, the site will automatically generate a PDF from all uploaded layout PDFs. Use sparingly. (To keep from accidentally rendering PDFs more often than we need, this box will automatically uncheck itself once the PDF has been created.)')
    issue_pdf_link = models.CharField(max_length=250, blank=True, null=True)
    submit_to_issuu = models.BooleanField('Submit PDF to Issuu', default=False, help_text='If you check this box, the site will automatically submit the PDF of this issue to Issuu (so that it can be displayed as a flip-book). Use sparingly. (To keep from accidentally submitting PDFs more often than we need, this box will automatically uncheck itself once the PDF has been sent to Issuu.) <strong>Note: You must create a PDF of this issue <em>before</em> you select this option.</strong>')
    issuu_id = models.CharField(max_length=250, blank=True, null=True)
    pdf_converted = models.BooleanField('Has the PDF converted?', default=False, help_text='Has the submitted PDF been successfully converted on Issuu?')

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

    def __unicode__(self):
        if self.name:
            return self.name
        elif self.old_archive:
            return u'Archive for %s' % self.pub_date
        elif self.online_update:
            return u'%s v. %s, Update %s/%s' % (self.volume.publication, self.volume.volume_id, self.pub_date.month, self.pub_date.day)
        else:
            return u'%s v. %s, Issue %s' % (self.volume.publication, self.volume.volume_id, self.issue_id)

    def save(self, *args, **kwargs):
        if self.render_issue_pdf:
            concat = PdfFileWriter()
            layout_count = self.layout_set.count()
            layouts = self.layout_set.all()[:layout_count]
            for layout in layouts:
                pagePDF = PdfFileReader(layout.PDF)
                concat.addPage(pagePDF.getPage(0))
            filename = 'vol%sissue%s.pdf' % (self.volume.volume_id, self.issue_id)
            filepath = '%s%s' % (settings.MEDIA_ROOT, filename)
            outputStream = file(filepath, 'wb')
            concat.write(outputStream)
            self.issue_pdf_link = '%s%s' % (settings.MEDIA_URL, filename)
            self.render_issue_pdf = False
        if self.submit_to_issuu and self.issue_pdf_link:
            issuu_data = [
                'action=issuu.document.url_upload',
                'apiKey=%s'  % settings.ISSUU_API_KEY,
                'category=009000',
                'commentsAllowed=false',
                'description=%s' % self.pub_date.strftime("%A, %B %e, %Y"),
                'downloadable=true',
                'explicit=false',
                'format=json',
                'infoLink=%s' % self.volume.publication.site.domain,
                'language=en',
                'name=vol%sissue%s' % (self.volume.volume_id, self.issue_id),
                'publishDate=%s' % self.pub_date.strftime("%Y-%m-%d"),
                'slurpUrl=%s' % self.issue_pdf_link,
                'tags=college newspapers,missouri,mizzou,news,the man-eater,university of missouri',
                'title=The Maneater -- Volume %s, Issue %s' % (self.volume.volume_id, self.issue_id),
                'type=007000',
            ]
            signature = ''
            for datum in issuu_data:
                datum_formatted = datum.replace('=', '')
                signature = signature + datum_formatted
            signature= '%s%s' % (settings.ISSUU_SECRET_KEY, signature)
            signature = hashlib.md5(signature).hexdigest()
            url = 'http://api.issuu.com/1_0?'
            for datum in issuu_data:
                url = url + datum.replace(' ', '%20') + '&'
            url = url + 'signature=' + signature
            json = urllib2.urlopen(url).read()
            document_id = simplejson.loads(json)['rsp']['_content']['document']['documentId']
            self.issuu_id = document_id
        if self.issuu_id and not self.pdf_converted and not self.submit_to_issuu:
            issuu_data = [
                'action=issuu.document.update',
                'apiKey=%s' % settings.ISSUU_API_KEY,
                'format=json',
                'name=vol%sissue%s' % (self.volume.volume_id, self.issue_id),
            ]
            signature = ''

            for datum in issuu_data:
                datum_formatted = datum.replace('=', '')
                signature = signature + datum_formatted

            signature = '%s%s' % (settings.ISSUU_SECRET_KEY, signature)
            signature = hashlib.md5(signature).hexdigest()
            url = 'http://api.issuu.com/1_0?'

            for datum in issuu_data:
                url = url + datum.replace(' ', '%20') + '&'

            url = url + 'signature=' + signature
            json = urllib2.urlopen(url).read()

            status = simplejson.loads(json)['rsp']['_content']['document']['state']

            if status == 'A':
                self.pdf_converted = True
            elif status == 'P':
                self.pdf_converted = False
            elif status == 'F':
                self.pdf_converted = False
                self.issuu_id = ''
        self.submit_to_issuu = False
        super(Issue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/issues/%s/' % self.id
