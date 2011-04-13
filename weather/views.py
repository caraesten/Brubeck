# Imports from standard libraries
from datetime import datetime
import urllib
from brubeck.settings import DEFAULT_METAR_STATION

# Imports from other dependencies
from metar import Metar

# cloudy, partlycloudy, rainy, snowy, sunny, [foggy, windy, hot, cold]

# Default weather station. maneater.weather uses aviation routine weather
# reports (METAR), so this setting should be a four-character ICAO airport 
# code--NOT the three-letter IATA code you're probably used to. For example,
# Lambert-St. Louis International Airport would be KSTL, not STL.
# Columbia Regional Airport is KCOU, not COU. 
# For more: http://en.wikipedia.org/wiki/List_of_airports_by_ICAO_code

def get_weather(station=DEFAULT_METAR_STATION):
    """
    Loads the latest METAR (aviation routine weather report) for the given
    station transmitted to the U.S. National Oceanic and Atmospheric 
    Administration. 
    The results of this function should be cached; since METAR reports are 
    generally updated hourly, and running this takes the better part of a second
    anyway (at least on my 2006 Dell), so anything using this information should
    probably cache it for, say, 20 or 30 minutes. No sense using all those 
    cycles every single pageview. (The last thing we need is a government agency
    thinking we're trying to run a denial-of-service attack on them.)
    """
    BASE_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations"
    station = station.upper()
    url = "%s/%s.TXT" % (BASE_URL, station)
    metar_file = urllib.urlopen(url)
    metar_code = ''
    
    # The file will usually have two lines--one with a date and time, and one
    # with the actual METAR code.
    for line in metar_file:
        if line.startswith(station):
            metar_code = line.strip()
    metar_file.close()
    
    metar = Metar.Metar(metar_code)
    
    snow = False
    rain = False
    fog = False
    clouds = False
    wind_speed = None
    wind_dir = None
    temperature = None
    
    weather = metar.weather
    
    for group in weather:
        # DZ: drizzle, RA: rain, SN: snow, SG: snow grains, IC: ice crystals,
        # PL: ice pellets, GR: hail, GS: snow pellets, UP: unknown, //: n/a
        if group[2] in ['DZ', 'RA', 'IC', 'PL', 'GR', '-DZ', '-RA', '-IC', '-PL', '-GR', '+DZ', '+RA', '+IC', '+PL', '+GR']:
            rain = True
        if group[2] in ['SN', 'SG', 'GS', '-SN', '-SG', '-GS', '+SN', '+SG', '+GS']:
            snow = True
        
        # BR: mist, FG: fog, FU: smoke, VA: volcanic ash, DU: dust, SA: sand,
        # HZ: haze, PY: spray
        if group[3] in ['BR', 'FG', 'HZ']:
            fog = True
    
    sky = metar.sky
    
    for group in sky:
        # cloud: anything, really, is going to be cloudy.
        if group[2]:
            clouds = True
        
        # cover: SKC: clear, CLR: clear, NSC: clear, NCD: clear, FEW: a few,
        #        OVC: overcast, SCT: scattered, BKN: broken, ///: n/a, 
        #        VV: indefinite ceiling
        if group[0] in ['FEW', 'SCT', 'BKN', 'OVC']:
            clouds = 'partly'
    
    try:
        wind_speed = int(round(metar.wind_speed.value('MPH')))
    except (TypeError, ValueError):
        wind_speed = None
    wind_dir = metar.wind_dir.compass()
    try:
        temperature_fahrenheit = int(round(metar.temp.value('F')))
    except (TypeError, ValueError):
        temperature_fahrenheit = None
    try:
        temperature_celsius = int(round(metar.temp.value('C')))
    except (TypeError, ValueError):
        temperature_celsius = None
    
    condition = 'clear'
    if clouds:
        condition = 'cloudy'
    if fog:
        condition = 'foggy'
    if wind_speed > 15:
        condition = 'windy'
    if snow:
        condition = 'snowy'
    if rain:
        condition = 'rainy'
    
    if condition in ['clear', 'cloudy', 'partlycloudy']:
        now = datetime.now().time().hour
        if now >= 7 and now <= 19:
            condition += '-day'
        else:
            condition += '-night'
    
    data = {
        'condition': condition,
        'temperature_fahrenheit': temperature_fahrenheit,
        'temperature_celsius': temperature_celsius,
        'wind_dir': wind_dir,
        'wind_speed': wind_speed
    }
    
    return data

