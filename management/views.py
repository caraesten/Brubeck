# Imports from standardized libraries
from datetime import date, timedelta
import datetime

# Imports from other installed libraries
from googleanalytics import Connection

# Imports from Django
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.articles.models import Article
from brubeck.blogs.models import Blog, Entry
from brubeck.design.models import Graphic, Layout
from brubeck.events.models import Event
from brubeck.management.models import WebFront
from brubeck.mapping.models import Map
from brubeck.multimedia.models import AudioClip, Slideshow, Video
from brubeck.photography.models import Photo
from brubeck.podcasts.models import Channel, Episode
from brubeck.publishing.models import Issue, Section
from brubeck.tagging.models import Tag
from brubeck.voxpopuli.models import Poll

@cache_page(60 * 5)
def top_online(request):

    connection = Connection(settings.ANALYTICS_EMAIL_ADDRESS, settings.ANALYTICS_EMAIL_PASSWORD)

    account = connection.get_accounts()[0]

    today = datetime.datetime.today()

    issues = Issue.objects.all().order_by('-pub_date').filter(online_update=0).filter(pub_date__lte=today)

#    start = issues[1].pub_date.date()

#    end = issues[0].pub_date.date()-timedelta(days=1)

    start = issues[0].pub_date.date()

    end = datetime.date.today()

    top_hits = account.get_data(start_date=start, end_date=end, dimensions=['pagePath',], metrics=['pageviews',], sort=['-pageviews',])

    top_hits_list = top_hits.tuple[:25]

    top_pages = account.get_data(start_date=start, end_date=end, dimensions=['pageTitle','pagePath',], metrics=['pageviews',], sort=['-pageviews',])

    top_pages_list = top_pages.tuple[:25]

    allowed_url_bases = ['audio', 'blogs', 'calendar', 'graphics', 'layouts', 'maps', 'photos', 'podcasts', 'polls', 'slideshows', 'stories', 'videos']

    top_content = []
    for entry in top_hits_list:
        substring = entry[0][0].split('/')
        if substring[1] in allowed_url_bases:
            top_content.append((entry, substring[1]))

    top_online = []
    for entry in top_content:
        if entry[1] == 'audio':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                audioclip = AudioClip.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(audioclip)
            except:
                pass
        elif entry[1] == 'blogs':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[3]
                month = substring[4]
                day = substring[5]
                slug = substring[6]
                entry = Entry.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(slug=slug)
                top_online.append(entry)
            except:
                pass
        elif entry[1] == 'calendar':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                slug = substring[5]
                event = Event.objects.filter(start__year=year).filter(start__month=month).filter(start__day=day).get(slug=slug)
                top_online.append(event)
            except:
                pass
        elif entry[1] == 'graphics':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                graphic = Graphic.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(graphic)
            except:
                pass
        elif entry[1] == 'layouts':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                layout = Layout.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(layout)
            except:
                pass
        elif entry[1] == 'maps':
            try:
                substring = entry[0][0][0].split('/')
                slug = substring[2]
                map = Poll.objects.get(slug=slug)
                top_online.append(map)
            except:
                pass
        elif entry[1] == 'photos':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                photo = Photo.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(photo)
            except:
                pass
        elif entry[1] == 'podcasts':
            try:
                substring = entry[0][0][0].split('/')
                id = substring[3]
                episode = Episode.objects.get(id=id)
                top_online.append(episode)
            except:
                pass
        elif entry[1] == 'polls':
            try:
                substring = entry[0][0][0].split('/')
                id = substring[2]
                poll = Poll.objects.get(id=id)
                top_online.append(poll)
            except:
                pass
        elif entry[1] == 'slideshows':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                slideshow = Slideshow.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(slideshow)
            except:
                pass
        elif entry[1] == 'stories':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                slug = substring[5]
                article = Article.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(slug=slug)
                top_online.append(article)
            except:
                pass
        elif entry[1] == 'videos':
            try:
                substring = entry[0][0][0].split('/')
                year = substring[2]
                month = substring[3]
                day = substring[4]
                id = substring[5]
                video = Video.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
                top_online.append(video)
            except:
                pass
                
    top_online = top_online[:10]

    page = {
        'end': end,
        'start': start,
        'top_content': top_content,
        'top_hits_list': top_hits_list,
        'top_online': top_online,
        'top_pages_list': top_pages_list,
    }

    return render_to_response('management/top_online.html', page, context_instance=RequestContext(request))

@cache_page(60 * 10)
def section_front(request, slug=None, page=1):
    """ 
    Shows a paginated list of articles for a given section.
    """
    site = Site.objects.get_current()
    try:
        section = Section.objects.filter(publication__site=site).get(slug=slug)
    except Section.DoesNotExist:
        raise Http404
    
    try:
        section_front = WebFront.objects.filter(site=site, type='section').get(top_sections=section)
        lead_item = section_front.item_set.all()[0]
        priority_items = section_front.item_set.all()[1:5]
    except WebFront.DoesNotExist:
        raise Http404

    archive_name = section.name

    try:
        page = int(page)
    except ValueError:
        raise Http404

    articles = Article.get_published.filter(section=section).exclude(webfronts__webfront=section_front)[:10]

    blog_posts = Entry.get_published.filter(blog__section=section)[:5]

    recent_articles = Article.get_published.filter(section=section)[:50]

    related_blogs = Blog.current.filter(section=section)

    related_podcasts = Episode.objects.filter(channel__section=section)[:5]

    tag_dict = {}
    for article in recent_articles:
        for tag in article.tags.all():
            if tag.title in tag_dict:
                tag_dict[tag.title] = tag_dict[tag.title] + 1
            else:
                tag_dict[tag.title] = 1

    featured_tags = tag_dict.items()

    ordered_tags = sorted(featured_tags, key=lambda tag: tag[1], reverse=True)[:30]

    tag_objects = []
    for tag in ordered_tags:
        tag_obj = Tag.objects.get(title=tag[0])
        tag_objects.append((tag_obj, tag[1]))

    random.shuffle(tag_objects)

    tag_cloud = []
    for tag in tag_objects:
        if tag[1] > 15:
            new_size = 25
        else:
            new_size = 9 + tag[1]
        tag_cloud.append((tag[0], new_size))

    page = {
        'archive_name': archive_name,
        'articles': articles,
        'blog_posts': blog_posts,
        'lead_item': lead_item,
        'ordered_tags': ordered_tags,
        'priority_items': priority_items,
        'related_blogs': related_blogs,
        'related_podcasts': related_podcasts,
        'section': section,
        'section_front': section_front,
        'tag_cloud': tag_cloud,
    }
    
    return render_to_response('management/section_front.html', page, RequestContext(request))
