# Imports from Django
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# Imports from brubeck
from brubeck.advertising.models import InfoPage
from brubeck.advertising.forms import RequestForm
from brubeck.emailing.views import render_email_and_send

def show_infopage(request):
    """
    Displays the most recently updated InfoPage instance and processes any
    requests for more information.
    """
    try:
        infopage = InfoPage.objects.latest()
    except InfoPage.DoesNotExist:
        raise Http404
    
    infopage.links = infopage.additionallink_set.all()
    
    remote_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        form = RequestForm(remote_ip, request.POST)
        if form.is_valid():
            render_email_and_send(message_template='advertising/request_info.txt', context=form.cleaned_data, subject="Request for advertising information", recipients=[settings.EDITORS['business']])
            return HttpResponseRedirect('/thanks/')
    else:
        form = RequestForm(remote_ip)
    
    page = {
        'form': form,
        'infopage': infopage
    }
    
    return render_to_response('advertising/show_infopage.html', page, context_instance=RequestContext(request))

