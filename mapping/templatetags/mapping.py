# Imports from Django
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

# Imports from brubeck
from brubeck.articles.models import Article
from brubeck.mapping.models import Map, Place

register = template.Library()

@register.simple_tag
def add_gmap_api():
    """
    Adds the site-wide JavaScript code for the Google Maps API.
    """
    return mark_safe('<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s&sensor=false" type="text/javascript"></script>' % settings.MAP_API_KEY)

@register.inclusion_tag('mapping/render_map_js.html')
def render_map_js(id=None, width=300, height=300):
    """
    Renders the js necessary to embed a given map object.
    """
    id = int(id)

    map = Map.objects.get(id=id)

    mpl_list = map.mapplacelink_set.all()

    latitudes = []
    longitudes = []

    for mpl in mpl_list:
        latitudes.append(float(mpl.place.coords.lat))
        longitudes.append(float(mpl.place.coords.lng))

    extents = {
        'min_lat': min(latitudes),
        'max_lat': max(latitudes),
        'min_lng': min(longitudes),
        'max_lng': max(longitudes)
    }

    return {
        'extents': extents,
        'height': height,
        'width': width,
    }

@register.inclusion_tag('mapping/render_map.html')
def render_map(id=None):
    """
    Renders a map and its associated places.
    """
    id = int(id)

    map = Map.objects.get(id=id)

    mpl_list = map.mapplacelink_set.all()

    return {
        'map': map,
        'mpl_list': mpl_list,
    }

@register.inclusion_tag('mapping/render_map_only.html')
def render_map_only(id=None):
    """
    Renders only the actual map requested.
    """
    id = int(id)

    map = Map.objects.get(id=id)

    mpl_list = map.mapplacelink_set.all()
       
    return {
        'map': map,
        'mpl_list': mpl_list,
    }
