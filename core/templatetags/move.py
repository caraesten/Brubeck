# Imports from standard libraries
from datetime import datetime
import operator
import random

# Imports from other python libraries
import twitter 

# Imports from Django
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.shortcuts import get_object_or_404

# Imports from maneater
from maneater.core.models import Article, Issue, MoveApproves, WebFront
from maneater.events.models import Calendar, Event
from maneater.multimedia.models import Slideshow, Video

register = template.Library()

@register.inclusion_tag('render_calendar.html')
def render_calendar(slug, title=None):
    """
    Shows the next five upcoming events from the calendar with the provided
    slug. The rendered.
    """
    cache_name = 'calendar-%s-events' % slug
    events = cache.get(cache_name)

    if title == 'None':
        title = None

    if not events:
        try:
            calendar = Calendar.objects.get(slug=slug)
            events = Event.not_past.filter(calendars=calendar)[:5]
            cache.set(cache_name, events, 60 * 10)
        except:
            events = None
    
    return {
        'events': events,
        'title': title,
    }

@register.inclusion_tag('latest_multimedia.html')
def latest_multimedia():
    """
    Shows the latest video or slideshow attached to an article from the current
    site.
    """
    site = Site.objects.get_current()
    
    cache_name = 'latest-multimedia-%s' % site.id
    latest_multimedia = cache.get(cache_name)
    
    if not latest_multimedia:
        try:
            try:
                latest_video = Video.objects.filter(publication__site=site).latest()
            except:
                latest_video = None
            try:
                latest_slideshow = Slideshow.objects.filter(publication__site=site).latest()
            except:
                latest_slideshow = None
            try:
                latest_audioclip = AudioClip.objects.filter(publication__site=site).latest()
            except:
                latest_audioclip = None
            
            if latest_video and latest_slideshow:
                if latest_slideshow.pub_date > latest_video.pub_date:
                    latest_multimedia = latest_slideshow
                else:
                    latest_multimedia = latest_video
            elif latest_video and not latest_slideshow:
                latest_multimedia = latest_video
            elif latest_slideshow and not latest_video:
                latest_multimedia = latest_slideshow
            else:  # neither a video nor a slideshow available
                latest_multimedia = None

            if latest_multimedia and latest_audioclip:
                if latest_audioclip.pub_date > latest_multimedia.pub_date:
                    latest_multimedia = latest_audioclip
                else:
                    latest_multimedia = latest_multimedia
            elif latest_multimedia and not latest_audioclip:
                latest_multimedia = latest_multimedia
            elif latest_audioclip and not latest_multimedia:
                latest_multimedia = latest_audioclip
            else:
                latest_multimedia = None

            if latest_multimedia:
                cache.set(cache_name, latest_multimedia, 60 * 5)
        except:
            latest_multimedia = None
    
    return {
        'latest_multimedia': latest_multimedia
    }

@register.inclusion_tag('random_stories.html')
def random_stories():
    """
    Picks five random published, non-future stories from the given Issue
    instance or later.
    """
    site = Site.objects.get_current()
    
    cache_name = 'random-stories-%s' % site.id
    try:
        articles = cache.get(cache_name)
    except:
        articles = None
    
    if not articles:
        try:
            front = WebFront.objects.filter(site=site).latest()
            issue = front.issue
            articles = Article.get_published.filter(section__publication__site=site).filter(issue__pub_date__gte=issue.pub_date).filter(issue__pub_date__lte=datetime.now())
            try:
                articles = random.sample(articles, 5)
            except ValueError:
                # If the desired sample size is greater than the number of
                # available articles, just pick all of them instead.
                articles = articles
            cache.set(cache_name, articles, 60 * 1)
        except:
            articles = None
    
    return {
        'articles': articles
    }

@register.inclusion_tag('latest_issue.html')
def latest_issue():
    """
    Shows the latest MOVE front page.
    """

    site = Site.objects.get_current()
    
    cache_name = 'MOVE-front-page'
    try:
        issue_front = cache.get(cache_name)
    except:
        issue_front = None
    
    if not issue_front:
        # Retrieve the latest issue of MOVE.
        front = WebFront.objects.filter(site=site).latest()
        issue = front.issue
        # Attempt to get the front page from the latest issue.
        try:
            issue_front = issue.layout_set.filter(type='cover').filter(section__publication__site=site)[0]
            cache.set(cache_name, issue_front, 60 * 1)
        except:
            issue_front = None
    
    return {
        'issue_front': issue_front,
    }

@register.inclusion_tag('dynamic_css.html')
def dynamic_css():
    """
    Renders custom style code 
    """

    site = Site.objects.get_current()
    front = WebFront.objects.filter(site=site).latest()
    issue = front.issue

    try:
        color = issue.color
    except:
	color = 990033

    return {
        'color': color,
    }

@register.inclusion_tag('site_color.html')
def site_color():
    """
    Renders custom style code
    """
       
    site = Site.objects.get_current()
    front = WebFront.objects.filter(site=site).latest()
    issue = front.issue
    
    try:
    	color = issue.color
    except:
	color = 990033

    return {
	'color': color,
    }

@register.inclusion_tag('masthead_image.html')
def masthead_image():
    """
    Renders custom style code
    """

    site = Site.objects.get_current()
    front = WebFront.objects.filter(site=site).latest()
    issue = front.issue

    return {
	'issue': issue,
    }
    
@register.inclusion_tag('latest_tweets.html')
def latest_tweets():
    """
    Shows the five most recent posts to the 'maneaterMOVE' Twitter account.
    """
    
    twitter_api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
    tweets_maneatermove = twitter_api.GetUserTimeline('maneatermove')[:5]
    
    return {
        'tweets_maneatermove': tweets_maneatermove,
    }
    
@register.inclusion_tag('render_rail.html')
def render_rail():
    """
    Shows the Web site rail, with relevant MOVE Approves content.
    """
    site = Site.objects.get_current()
    
    cache_name = 'MOVE-Approves-content'
    try:
        MOVE_Approves = cache.get(cache_name)
    except:
        MOVE_Approves = None
    
    if not MOVE_Approves:
        # Retrieve the latest issue of MOVE.
        front = WebFront.objects.filter(site=site).latest()
        issue = front.issue
        # Attempt to get the front page from the latest issue.
        try:
            MOVE_Approves = MoveApproves.objects.filter(pub_date__gte=issue.pub_date)
            cache.set(cache_name, MOVE_Approves, 60 * 5)
        except:
            MOVE_Approves = None
            
    return {
        'MOVE_Approves': MOVE_Approves,
    }

@register.inclusion_tag('core/twitter_list.html')
def render_tweets(limit=None):
    """
    Pulls the latest five tweets from MOVE's Twitter account(s)
    and sorts them by the date they were posted, from newest to
    oldest.
    """

    cache_name = 'compiled-move-tweets'
    tweet_list = cache.get(cache_name)

    if not tweet_list:
        try:
            """
            Try to import the Twitter accounts listed in settings.
            """
            twitter_accounts = settings.TWITTER_ACCOUNTS
        except:
            """
            If there are no Twitter accounts in settings, just use the
            default account.
            """
            twitter_accounts = (
                ('maneatermove', 'gnomes&PBR'),
            )

        try:
            twitter_api = twitter.Api(username=settings.TWITTER_ACCOUNTS[0][0], password=settings.TWITTER_ACCOUNTS[0][1])
            unordered_tweets = []
            for account in twitter_accounts:
                unordered_tweets.extend(twitter_api.GetUserTimeline(account[0])[:5])
            tweet_times = []
            for tweet in unordered_tweets:
                tweet_times.append((tweet.created_at_in_seconds, tweet))
            map(operator.itemgetter(0), tweet_times)
            ordered_tweets = sorted(tweet_times,key=operator.itemgetter(0), reverse=True)
            tweet_list = []
            for tweet in ordered_tweets:
                tweet_list.append(tweet[1])
            cache.set(cache_name, tweet_list, 60 * 10)
        except:
            tweet_list = None

    if limit:
        try:
            limit = int(limit)
            tweet_list = tweet_list[:limit]
        except:
            pass

    return {
        'tweet_list': tweet_list
    }