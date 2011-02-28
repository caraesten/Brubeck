# Imports from standard libraries
from datetime import date

# Imports from Django
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q
from django.utils.html import urlize

# Advertisements
class CurrentManager(models.Manager):
    """
    Only returns ads that are currently active; i.e., they have started but not 
    ended).
    The last filter() statement takes an OR (|) operator because an ad with a 
    null end_date is always considered active. For information on the Q object
    syntax here, see:
    http://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    """
    def get_query_set(self):
        TODAY = date.today()
        return super(CurrentManager, self).get_query_set().filter(start_date__lte=TODAY).filter(Q(end_date__isnull=True) | Q(end_date__gte=TODAY))

class BannerAd(models.Model):
    """
    Manages the display of banner ads.
    """
    AD_CHOICES = (
        ('vertical', "Sidebar: Vertical Skyscraper"),
        ('shortvert', "Sidebar: Short Vertical"),
        ('banner', "Content Foot: Horizontal Banner"),
        ('cube', "Front Page: Cube"),
        ('eyebrow', "Sitewide: Eyebrow"),
    )
    name = models.CharField(max_length=75, help_text="If this is an image ad, this becomes the tooltip text (what you see when you hover over the ad).")
    start_date = models.DateField(db_index=True)
    # FIXME: This did not have null=True in the 2008 site. Change this in the 
    # database.
    end_date = models.DateField(db_index=True, blank=True, null=True, help_text="Inclusive, i.e., this is the last date on which this ad will be seen. <strong>Note:</strong> If you leave this field blank, the ad will run indefinitely.")
    site = models.ForeignKey(Site, db_index=True)
    ad_type = models.CharField(max_length=9, choices=AD_CHOICES, help_text="The size and shape of this ad. Our slots use the following <a href=\"http://www.iab.net/iab_products_and_industry_services/1421/1443/1452\">IAB</a> or <a href=\"https://www.google.com/adsense/static/en_US/AdFormats.html\">Google</a> ad sizes.<ul><li>Vertical skyscraper ads show in the sidebar and are usually 160x600 pixels (wide skyscraper). These don't show up on the front page, but they do show up in most listing/index/archive pages. <strong>No more than 170 pixels wide. If it's shorter than 250 pixels high, make it a \"short vertical\".</strong></li><li>Short vertical ads show in the sidebar (just like vertical skyscrapers) and are normally 120x240 pixels. <strong>No more than 250 pixels high. No more than 170 pixels wide.</strong></li><li>Horizontal banner ads show up at the bottom of most pages (and appear on the front page). They range from 234x60 pixels (half banner) to 468x60 pixels (banner). <strong>No more than 500 pixels wide.</strong></li><li>Eyebrow ads appear at the top of every page, next to our flag and the weather icons. They are always 234 pixels wide by 60 pixels tall (note this is the same size as a half banner ad). <strong>Double-check every eyebrow ad's dimensions and information before you save it, as it will be shown on every page if you mess up.</strong></li><li>'Cube' ads show up next to Top Multimedia and Latest Tweets on our front page. They are always 300 pixels wide by 250 pixels tall. <strong>Double-check every cube ad's dimensions before you save it.</strong></li></ul>")
    # FIXME: This had null=True in the 2008 site. Change this in the database.
    url = models.URLField('link', max_length=200, blank=True, verify_exists=False, help_text="If this ad is a link to something, enter the URL here. Only works for image-based ads. <strong>Note:</strong> Use the full URL, <strong>including the <em>http://</em> portion</strong>; i.e., <em>http://www.themaneater.com/</em>")
    # FIXME: This had null=True in the 2008 site. Change this in the database.
    image = models.ImageField(upload_to='%Y/%m%d/ads', blank=True, help_text="If this is an image ad, upload the image here. Accepts JPEG, GIF or PNG file formats. <strong>Please resize the image to follow the guidelines above <em>before uploading</em></strong>. If you don't and the image is too large, the site will attempt to resize the image on its own, but the online staff makes no guarantees it will do so correctly. If the site complains about this field and asks you to \"upload a valid image\", open the file in Photoshop and re-save it as a JPEG.")
    # FIXME: This had null=True in the 2008 site. Change this in the database.
    code = models.TextField(blank=True, help_text="If this is actually a JavaScript-based ad (such as Google AdSense) or a Flash-based ad, enter the code here. (Flash-based ads require the file to be uploaded on the server. If you need to post a Flash-based ad, e-mail the online staff to set up the ad for you.) <strong>Note:</strong> If anything is in this field, the image field is ignored. <em>An ad requires either an image or code to show up.</em>")
    
    objects = models.Manager()
    current = CurrentManager()
    
    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = 'start_date'
        ordering = ['-end_date', '-start_date']
