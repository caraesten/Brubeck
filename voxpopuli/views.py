from datetime import datetime, time

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from brubeck.voxpopuli.forms import PollForm
from brubeck.voxpopuli.models import Choice, Poll, Survey, Vote

def vote_id(request):
    try:
        user_agent = request.META['HTTP_USER_AGENT']
    except KeyError:
        user_agent = 'unknown'
    return slugify('onsite-%s-%s' % (request.META['REMOTE_ADDR'], user_agent))[:255]

def poll_vote(request, id=None):
    show_results = False
    
    poll = get_object_or_404(Poll, id=id)
    unique_id = vote_id(request)
    already_voted = Vote.objects.filter(poll=poll, unique_id=unique_id).count()
    
    if poll.voting_open and not already_voted:
        if request.method == 'POST':
            form = PollForm(request.POST, poll_id=id)
            if form.is_valid():
                else:
                    choice = get_object_or_404(Choice, id=int(form.cleaned_data['choice']))
                    new_vote = Vote(poll=poll, vote=choice, unique_id=unique_id)
                    new_vote.save()
                show_results = True
        else:
            form = PollForm(poll_id=id)
    else:
        show_results = True
    
    if show_results:
        return HttpResponseRedirect(reverse('voxpopuli-poll-results', kwargs={'id': id}))
    
    page = {
        'form': form,
        'poll': poll,
    }
    
    return render_to_response('voxpopuli/poll_vote.html', page, context_instance=RequestContext(request))

def poll_results(request, id=None):
    poll = get_object_or_404(Poll, id=id)
    results = Choice.objects.filter(poll=poll).annotate(num_votes=Count('vote')).order_by('-num_votes')
    
    unique_id = vote_id(request)
    already_voted = Vote.objects.filter(poll=poll, unique_id=unique_id).count()
    
    page = {
        'already_voted': already_voted,
        'poll': poll,
        'results': results,
    }
    
    return render_to_response('voxpopuli/poll_results.html', page, context_instance=RequestContext(request))

