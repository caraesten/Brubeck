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

def survey_vote(request, slug=None):
    show_results = False
    
    survey = get_object_or_404(Survey, slug=slug)
    
    unique_id = vote_id(request)
    
    questions = []
    for question in survey.questions.all():
        already_voted = Vote.objects.filter(poll=question, unique_id=unique_id).count()
        if not already_voted:
            if request.method == 'POST':
                form = PollForm(poll_id=question.id, prefix=question.slug, data=request.POST)
                if form.is_valid():
                    choice = Choice.objects.get(id=int(form.cleaned_data['choice']))
                    new_vote = Vote(poll=question, vote=choice, unique_id=unique_id)
                    new_vote.save()
                    show_results = True
            else:
                form = PollForm(poll_id=question.id, prefix=question.slug)
                questions.append((question, form))
    if not questions:
        show_results = True
    
    if show_results:
        return HttpResponseRedirect(reverse('voxpopuli-survey-results', kwargs={'slug': slug}))
    
    page = {
        'questions': questions,
        'survey': survey,
    }
    
    return render_to_response('voxpopuli/survey_vote.html', page, context_instance=RequestContext(request))

def survey_results(request, slug=None):
    survey = get_object_or_404(Survey, slug=slug)
    unique_id = vote_id(request)
    
    results = []
    votes = []
    for question in survey.questions.all():
        results.append((question, Choice.objects.filter(poll=question).annotate(num_votes=Count('vote')).order_by('-num_votes')))
        votes.append(0 != Vote.objects.filter(poll=question, unique_id=unique_id).count())
    
    already_voted = False
    if True in votes:
        already_voted = True
    
    page = {
        'already_voted': already_voted,
        'results': results,
        'survey': survey,
    }
    
    return render_to_response('voxpopuli/survey_results.html', page, context_instance=RequestContext(request))
