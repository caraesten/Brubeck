# Imports from Django
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

# Imports from Django
from brubeck.reporters.models import SourceType

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def staff_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def staff_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def index_page(request):
    return direct_to_template(request, 'reporters/index_page.html')

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def source_list(request, type_slug):
    source_type = get_object_or_404(SourceType, slug=type_slug)
    sources = source_type.source_set.all()
    for source in sources:
        source.addresses = source.address_set.all()
        source.numbers = source.phonenumber_set.all()
    
    page = {
        'source_type': source_type,
        'sources': sources
    }
    
    return render_to_response('reporters/source_list.html', page, context_instance=RequestContext(request))

