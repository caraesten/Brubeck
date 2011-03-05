from django.contrib.gis.geos import Point

from brubeck.blotter.models import Location
from brubeck.campusguide.models import Place as CGPlace
from brubeck.mapping.models import Place, PointPlaceHolder

def interim_coords_assist():
    for place in Location.objects.all():
        coords = place.coords
        phpoint = Point(coords.lng, coords.lat)
        placeholder = PointPlaceHolder(
            point = phpoint,
            bl_id = place.id
        )
        placeholder.save()
    for place in CGPlace.objects.all():
        coords = place.coords
        phpoint = Point(coords.lng, coords.lat)
        placeholder = PointPlaceHolder(
            point = phpoint,
            cp_id = place.id
        )
        placeholder.save()
#     for place in Place.objects.all():
#         coords = place.coords
#         phpoint = Place(coords.lng, coords.lat)
#         placeholder = PointPlaceHolder(
#             point = phpoint,
#             mp_id = place.id
#         )
#         placeholder.save()