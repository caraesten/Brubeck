# Imports from Django
from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

# Imports from brubeck
from brubeck.articles.models import Article
from brubeck.mapping.models import Map, Place

def detail(request, slug=None, mode='context'):
    """
    Accesses a map and its associated places and, depending on mode, returns
    either a standalone page to show the map or a dictionary of the map data
    that can be added to an article's template context.
    """
    try:
        map = Map.objects.get(slug=slug)
    except Map.DoesNotExist:
        if mode == 'context':
            return None
        elif mode == 'page':
            raise Http404
        else:
            raise StandardError("mode must be either 'context' or 'page'")
    # HERE.
    # places = map.place_set.all()
    mpl_list = map.mapplacelink_set.all()
    # places = Place.objects.filter(mapplacelink__map=map)

    #places = []

    #for place_item in place_items:
    #    places.append(place_items.place)
    
    latitudes = []
    longitudes = []
    
    for mpl in mpl_list:
        latitudes.append(float(mpl.place.point.get_y()))
        longitudes.append(float(mpl.place.point.get_x()))
    
    extents = {
        'min_lat': min(latitudes),
        'max_lat': max(latitudes),
        'min_lng': min(longitudes),
        'max_lng': max(longitudes)
    }
    
    page = {
        'extents': extents,
        'map': map,
        'mpl_list': mpl_list,
    }
    
    if mode == 'context':
        return page
    elif mode == 'page':
        return render_to_response('mapping/detail.html', page, context_instance=RequestContext(request))
    else:
        raise StandardError("mode must be either 'context' or 'page'")
