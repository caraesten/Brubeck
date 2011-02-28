from django.contrib.gis.db import models

class Address(models.Model):
    """
    Organizes sources' various addresses.
    """
    ADDRESS_CHOICES = (
        ('work', "Work"),
        ('home', "Home"),
        ('other', "Other"),
    )
    type = models.CharField(max_length=5, choices=ADDRESS_CHOICES)
    address = models.ForeignKey('brubeck.geography.Place')

    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s: %s' % (self.source, self.type)

class PhoneNumber(models.Model):
    """
    Organizes sources' various phone numbers.
    """
    ADDRESS_CHOICES = (
        ('work', "Work"),
        ('home', "Home"),
        ('fax', "Fax"),
        ('cell', "Cell"),
        ('other', "Other"),
    )
    type = models.CharField(max_length=5, choices=ADDRESS_CHOICES)
    number = models.CharField(max_length=30)

    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s: %s' % (self.source, self.type)
