# Imports from standard libraries
from datetime import date, datetime, time, timedelta

# Imports from Django
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.http import urlencode

def redirect(request, url=None, type='permanent', extra=None):
    """
    Redirects a user to a given URL. Supports both HTTP 301 and HTTP 302.
    """

    if type == 'permanent':
        return HttpResponsePermanentRedirect(url)
    else:
        return HttpResponseRedirect(url)

def normalize_to_datetime(object):
    """
    Converts date objects into datetime objects to allow things to be more  
    easily compared.
    """
    if isinstance(object, date) and not isinstance(object, datetime):
        # Assume the article was published at midnight. This automatically
        # makes blog entries take precedence over articles that were published
        # on the same day.
        return datetime.combine(object, time.min)
    else:
        # Do nothing.
        return object
