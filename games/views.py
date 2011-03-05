# Imports from Django
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page

# Imports from brubeck
from brubeck.core.models import Issue
from brubeck.games.models import GameAnswer

@cache_page(60 * 20)
def detail(request, id=None):
    """
    Shows a specific game answer.
    """
    answer = get_object_or_404(GameAnswer, id=id)
    
    page = {
        'answer': answer
    }
    
    return render_to_response('games/detail.html', page, context_instance=RequestContext(request))

@cache_page(60 * 20)
def latest(request):
    """
    Shows the latest issue's game answers.
    """
    site = Site.objects.get_current()
    latest_issue = Issue.objects.filter(volume__publication__site=site).filter(online_update=False).latest()
    
    answers = GameAnswer.objects.filter(issue=latest_issue)
    
    page = {
        'answers': answers
    }
    
    return render_to_response('games/latest.html', page, context_instance=RequestContext(request))

