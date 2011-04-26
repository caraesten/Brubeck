# Imports from standard libraries
from datetime import date

# Imports from Django
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

# Imports from brubeck
from brubeck.articles.models import Article
from brubeck.multimedia.models import AudioClip, Slideshow, Video
from brubeck.podcasts.models import Channel, Episode

def detail(request, year=None, month=None, day=None, id=None, mediatype=None):
    """Show a specific video or slideshow."""
    # From an optimization standpoint, it makes no real sense to convert year,
    # month and day to integers outside the try/except block; since only one
    # mediatype can be chosen at any given time, this conversion will only
    # happen once anyway.
    try:
        if mediatype == 'video':
            object = Video.objects.filter(pub_date__year=int(year),pub_date__month=int(month), pub_date__day=int(day)).get(id=id)
        elif mediatype == 'slideshow':
            object = Slideshow.objects.filter(pub_date=date(int(year),int(month),int(day))).get(id=id)
        elif mediatype == 'audioclip':
            object = AudioClip.objects.filter(pub_date=date(int(year),int(month),int(day))).get(id=id)
        else:
            raise StandardError("mediatype must be 'video', 'slideshow' or 'audioclip'")
    except ObjectDoesNotExist:
        raise Http404
    
    # Convert length (given in seconds) into minutes and seconds, padding
    # the seconds with an extra zero if needed.
    object.minutes = object.length // 60
    object.seconds = object.length % 60
    if object.seconds < 10:
        object.seconds = '0' + str(object.seconds)
    
    # Get the latest few articles to include this item.
    site = Site.objects.get_current()
    articles = Article.get_published.filter(issue__volume__publication__site=site)
    if mediatype == 'video':
        articles = articles.filter(videos=object)[:3]
    elif mediatype == 'slideshow':
        articles = articles.filter(slideshows=object)[:3]
    elif mediatype == 'audioclip':
        articles = articles.filter(audio_clips=object)[:3]
    else:
        raise StandardError("mediatype must be 'video', 'slideshow' or 'audioclip'")
    
    page = {
        'articles': articles,
        'object': object
    }
    
    return render_to_response('multimedia/detail.html', page, context_instance=RequestContext(request))

@cache_page(60 * 5)
def top_multimedia(request, page=1):
    """Show a list of the 15 most recent audio clips, podcasts, slideshows and videos."""
    
    try:
        page = int(page)
    except ValueError:
        raise Http404
        
    site = Site.objects.get_current()
    channel_list = Channel.current.filter(section__publication__site=site)
    
    # Get the fifteen latest of each type.
    latest_audio_clips = AudioClip.objects.all().filter(publication__site=site)
    latest_podcast_episodes = Episode.objects.all().filter(channel__section__publication__site=site)
    latest_slideshows = Slideshow.objects.all().filter(publication__site=site)
    latest_videos = Video.objects.all().filter(publication__site=site)
    
    list = []
    list.extend(latest_audio_clips)
    list.extend(latest_podcast_episodes)
    list.extend(latest_slideshows)
    list.extend(latest_videos)
    
    list2 = []
    
    for item in list:
        try:
            datenew = item.pub_date.date()
        except:
            datenew = None
        if datenew:
            list2.append([datenew, [item.id, item.mediatype]])
        else:
            list2.append([item.pub_date, [item.id, item.mediatype]])

    list2.sort()
    
    list2.reverse()
    
    list3 = []
    
    for mm_piece in list2:
        piece_id = mm_piece[1][0]
        mediatype = mm_piece[1][1]
        if mediatype == 'audioclip':
            piece = AudioClip.objects.get(id=piece_id)
            list3.append(piece)
        elif mediatype == 'podcast':
            piece = Episode.objects.get(id=piece_id)
            list3.append(piece)
        elif mediatype == 'slideshow':
            piece = Slideshow.objects.get(id=piece_id)
            list3.append(piece)
        elif mediatype == 'video':
            piece = Video.objects.get(id=piece_id)
            list3.append(piece)

    # list = list().order_by('-pub_date')
    
    paginator = Paginator(list3, 20)
    
    page_count = paginator.num_pages
    
    archive_page = paginator.page(page)
    
    page = {
        'archive_page': archive_page,
        'channel_list': channel_list,
        'latest_audio_clips': latest_audio_clips,
        'latest_podcast_episodes': latest_podcast_episodes,
        'latest_slideshows': latest_slideshows,
        'latest_videos': latest_videos,
        'list2': list2,
        'list3': list3,
        'page': page,
        'page_count': page_count,
    }
    
    return render_to_response('multimedia/top_multimedia.html', page, context_instance=RequestContext(request))
