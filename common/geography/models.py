# Imports from standard libraries
import re
import sys

# Imports from other dependencies
from geopy import geocoders

# Imports from Django
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Imports from maneater
from brubeck.common.geography.fields import CoordinatesField

def geocode(location):
    """
    Uses the Google Maps geocoder to determine a location's coordinates. If the
    geocoder returns multiple results, choose the first one.
    """
    sys.stdout = open(settings.STDOUT_FILE, 'w')
    g = geocoders.Google(resource='maps')
    ends_with_zip = r'(?: \d{5}| \d{5}-\d{4})$'
    if not re.search(ends_with_zip, location):
        location += ', 65201'
    place, (lat, lng) = list(g.geocode(location, exactly_one=False))[0]
    sys.stdout = sys.__stdout__
    return Point(lng, lat)

class Place(models.Model):
    """
    Provides an abstract base class for other maps' point-based models.
    """
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=80, blank=True)
    lookup = models.BooleanField('look up coordinates?', default=False, help_text="Check this box if you'd like the site to use the provided address to look up the coordinates for this location when you save. <strong>If you do this:</strong> It is strongly suggested you click \"save and continue editing\" in order to check whether the site selected the point you actually intended. You might need to uncheck this box afterward and tweak the result.")
#     coords = CoordinatesField('coordinates', help_text="Center the map on the location to select coordinates.")
    # coords = LocationField('coordinates', default='%s,%s' % (settings.DEFAULT_LATITUDE, settings.DEFAULT_LONGITUDE), help_text="Center the map on the location to select coordinates.")
    point = models.PointField(blank=True, null=True)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    def save(self):
        """
        If requested, geocode the given address.
        """
        if self.lookup:
            try:
                self.point = geocode(self.address)
            except:
                self.name += ' (Geocoding error. Try choosing the coordinates directly.)'
        super(Place, self).save()
    
    class Meta:
        abstract = False
        ordering = ['name']
        
class Area(models.Model):
    """
    Provides a concrete base class for other area-based models.
    """
    name = models.CharField(max_length=60)
    area = models.MultiPolygonField()
    
    objects = models.GeoManager()

    class Meta:
        abstract = False
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
