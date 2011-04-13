# Imports from Django
from django import template
from django.core.cache import cache

# Imports from maneater
from brubeck.weather.views import get_weather

register = template.Library()

@register.inclusion_tag('weather/render_weather_graphic.html')
def render_weather_graphic():
    """
    Obtains the latest weather information.
    """
    weather = cache.get('maneater-views_frontpage-render-weather')
    if not weather:
        try:
            weather = get_weather()
            cache.set('maneater-views_frontpage-render-weather', weather, 60 * 20)
        except:
            weather = None
    return {
        'weather': weather
    }

