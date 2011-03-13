"""
Staff views

Allow users to view lists of all staffers (or just active ones) and individual
pages for each.

"""

# Imports from Django
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.personnel.models import Staffer, Tenure

@cache_page(60 * 60 * 1)
def staffers(request, page=1, mode='active'):
    """Show a list of staffers. mode determines which ones.
    
    By default, this view only shows staffers marked as active, though it also
    supports viewing all staffers and only editors.
    
    """
    try:
        page = int(page)
    except ValueError:
        raise Http404
    
    flatpage = None
    
    if mode == 'active':
        staff_list = Staffer.objects.filter(is_active=True)
    elif mode == 'editors':
        staff_list = Staffer.objects.filter(tenure__current=True).order_by('tenure__position')
        flatpage = FlatPage.objects.filter(sites__exact=Site.objects.get_current()).get(url='/staff/editors/business_staff/')
    elif mode == 'all':
        staff_list = Staffer.objects.all()
    else:
        raise Http404
    
    paginator = Paginator(staff_list, 25)
    
    try:
        staff_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    page = {
        'flatpage': flatpage,
        'mode': mode,
        'staff_page': staff_page
    }
    
    return render_to_response('personnel/staffers.html', page, context_instance=RequestContext(request))

@cache_page(60 * 60 * 1)
def detail(request, slug=None):
    """Show an individual staffer's portfolio page."""
    staffer = get_object_or_404(Staffer, slug=slug)
    
    page = {
        'staffer': staffer
    }
    
    return render_to_response('personnel/detail.html', page, context_instance=RequestContext(request))
