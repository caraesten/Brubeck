from django import forms
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

class Coordinates():
    def __init__(self, lat, lng):
        self.lat = float(lat)
        self.lng = float(lng)
    def __repr__(self):
        return ','.join([str(self.lat), str(self.lng)])
    lat = float()
    lng = float()

# NOTE: Came from http://www.djangosnippets.org/snippets/615/ (-JCM)

# The development of this code was sponsored by MIG Internacional
# This code is released under the terms of the BSD license
# http://code.djangoproject.com/browser/django/trunk/LICENSE
# Feel free to use it at your whim/will/risk :D
# Contact info: Javier Rojas <jerojasro@gmail.com>

class LocationWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        try:
            lat = value.lat
            lng = value.lng
        except AttributeError:
            lat = settings.DEFAULT_LATITUDE
            lng = settings.DEFAULT_LONGITUDE
        js = '''
        </script>
        <script type="text/javascript">
            //<![CDATA[
            var %(name)s_marker ;
            $(document).ready(function () {
                if (GBrowserIsCompatible()) {
                    var map = new GMap2(document.getElementById("map_%(name)s"));
                    map.setCenter(new GLatLng(%(default_lat)s,%(default_lng)s), 13);
                    %(name)s_marker = new GMarker(new GLatLng(%(default_lat)s,%(default_lng)s), {draggable: true});
                    map.addOverlay(%(name)s_marker);
                    map.addControl(new GLargeMapControl());
                    map.addControl(new GMapTypeControl());
                    $('#%(name)s_id')[0].value = %(name)s_marker.getLatLng().lat() + "," + %(name)s_marker.getLatLng().lng();
                    GEvent.addListener(%(name)s_marker, "dragend", function() {
                        var point = %(name)s_marker.getLatLng();
                        $('#%(name)s_id')[0].value = point.lat() + "," + point.lng();
                    });
                }});
            $(document).unload(function () {GUnload()});
            //]]>
        </script>
        ''' % {'name': name, 'default_lat': lat, 'default_lng': lng}
        # % dict(name=name)
        html = self.inner_widget.render("%s" % name, None, dict(id='%s_id' % name))
        html += "<div id=\"map_%s\" style=\"width: 500px; height: 500px\"></div>" % name
        return mark_safe(js+html)


class LocationField(forms.Field):
    widget = LocationWidget

    def clean(self, value):
        lat, lng = value.split(',')
        return Coordinates(lat, lng)

# My stuff again. (-JCM)

class CoordinatesField(models.Field):
    __metaclass__ = models.SubfieldBase
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 70
        kwargs['default'] = Coordinates(settings.DEFAULT_LATITUDE, settings.DEFAULT_LONGITUDE)
        super(CoordinatesField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if isinstance(value, Coordinates):
            return value
        lat, lng = value.split(',')
        return Coordinates(lat, lng)

    def get_db_prep_value(self, value, connection, prepared=True):
        return str(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': LocationField}
        defaults.update(kwargs)
        return super(CoordinatesField, self).formfield(**defaults)

    def db_type(self, connection):
        return 'varchar(70)'
        
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        lat, lng = str(value).split(',')
        return '%s, %s' % (str(lat).strip(), str(lng).strip())

