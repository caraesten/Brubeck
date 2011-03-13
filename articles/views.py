# Imports from standard libraries
from datetime import date, datetime, time, timedelta

# Imports from Django
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.articles.models import Article, Correction
from brubeck.mapping.views import detail as map_detail

@cache_page(60 * 5)
def archive(request, year=None, month=None, day=None, page=1):
    """
    Shows a paginated list of articles by year, month or day.
    
    Arguments:
        'year'
            Optional.
        'month'
            Optional.
        'day'
            Optional.
        'page'
            Optional.
    
    Context:
        'archive_name'
            A string with the name of the archive to display.
        'archive_page'
            A Paginator.page instance with object_list containing the articles
            to display.
    """
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)
    except ValueError:
        raise Http404
    
    site = Site.objects.get_current()
    
    try:
        articles = Article.get_published.filter(section__publication__site=site)
    except:
        raise Http404
    
    if not year:
        articles = articles
        archive_name = "Article archive"
    elif not month:
        articles = articles.filter(pub_date__year=year)
        archive_name = "Articles from %s" % year
    elif not day:
        articles = articles.filter(pub_date__year=year, pub_date__month=month)
        archive_name = "Articles from %s" % date(year, month, 1).strftime("%B %Y")
    else:
        articles = articles.filter(pub_date=date(year, month, day))
        archive_name = "Articles from %s" % date(year, month, day).strftime("%B %d, %Y")
    
    paginator = Paginator(articles, 20)
    
    try:
        archive_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404
    
    url_base = '/stories/'
    if year:
        url_base += '%s/' % year
    if month:
        url_base += '%s/' % month
    if day:
        url_base += '%s/' % day
    
    next_page_url = '%sp%s/' % (url_base, page + 1)
    previous_page_url = '%sp%s/' % (url_base, page - 1)
    
    page = {
        'archive_name': archive_name,
        'archive_page': archive_page,
        'next_page_url': next_page_url,
        'previous_page_url': previous_page_url
    }
    
    return render_to_response('core/archive.html', page, context_instance=RequestContext(request))

@cache_page(60 * 5)
def detail(request, year=None, month=None, day=None, slug=None, mode=None):
    """
    Shows a particular article or its associated photos and graphics.
    """
    site = Site.objects.get_current()
    try:
        article = Article.get_published.filter(section__publication__site=site).filter(pub_date__exact=date(int(year), int(month), int(day))).get(slug=slug)
    except Article.DoesNotExist:
        raise Http404
    
    images = []
    images.extend(article.photos.all())
    images.extend(article.editorial_cartoons.all())
    images.extend(article.graphics.all())
    
    multimedia = []
    multimedia.extend(article.videos.all())
    multimedia.extend(article.slideshows.all())
    multimedia.extend(article.audio_clips.all())
    multimedia.extend(article.podcast_episodes.all())
        
    if article.map:
        map_data = map_detail(request, slug=article.map.slug, mode='context')
    else:
        map_data = None
    
    if article.type == 'column':
        try:
            article.mugshot = article.byline[0].mugshot
        except:
            article.mugshot = None
    else:
        article.mugshot = None
    
    article.attached_audio = False
    for item in article.attached_files.all():
        if item.get_file_extension() == 'mp3':
            article.attached_audio = True
    
    page = {
        'article': article,
        'images': images,
        'map_data': map_data,
        'multimedia': multimedia
    }
    
    if mode == 'images':
        return render_to_response('articles/detail_images.html', page, context_instance=RequestContext(request))
    else:
        return render_to_response('articles/detail.html', page, context_instance=RequestContext(request))

def corrections(request):
    """
    Shows corrections from the past two weeks.
    """
    TWOWEEKSAGO = date.today() - timedelta(14)
    corrections = Correction.objects.filter(date_corrected__gte=TWOWEEKSAGO)

    page = {
        'corrections': corrections
    }

    return render_to_response('articles/correction_list.html', page, context_instance=RequestContext(request))
