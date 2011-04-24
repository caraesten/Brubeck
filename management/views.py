# -*- coding: utf-8 -*- 
# Imports from standard libraries
import calendar as pycal
from datetime import date, datetime, time, timedelta
import itertools
import operator

# Imports from Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.markup.templatetags.markup import markdown
from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import urlize
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page

# Imports from Brubeck
from brubeck.articles.models import Article
from brubeck.blogs.models import Blog, Entry
from brubeck.core import imaging
from brubeck.design.models import Graphic, Layout
from brubeck.events.models import Calendar, Event
from brubeck.management.models import NewsBurst, WebFront
from brubeck.mapping.models import Map
from brubeck.multimedia.models import AudioClip, Slideshow, Video
from brubeck.photography.models import Photo
from brubeck.podcasts.models import Channel, Episode
from brubeck.publishing.models import Issue, Section
from brubeck.tagging.models import Tag
from brubeck.voxpopuli.models import Poll

# Imports from other dependencies.
#from googleanalytics import Connection

@cache_page(60 * 1)
def render_frontpage(request):
	"""
	Retrieves the most recently updated front-page configuration from the 
	database and renders it.
	
	Since this view will process anywhere from a quarter to half our pageviews 
	for a given day, it should be pretty damn fast. Django's template language
	is nice, but doing processing there is much slower than doing it in the
	view--so let's do a fair amount of the rendering and processing before we
	get there.
	
	Template:
		frontpage.html
	
	Arguments:
		None.
	
	Context (let's fill this in soon):
		'all_blogs'
		'calendar'
		'calendar_list'
		'events'
		'event_list'
		'issue'
		'issue_front'
		'issue_other_layouts'
		'latest_audio'
		'latest_blog_posts'
		'latest_multimedia'
		'latest_online_exclusives'
		'latest_podcast_episodes'
		'latest_slideshow'
		'latest_video'
		'month'
		'month_formatted'
		'month_minus'
		'month_name'
		'month_plus'
		'news_bursts'
		'other_info'
		'rotating_item_list'
		'rotating_items'
		'section_arts'
		'section_arts_articles'
		'section_forum'
		'section_forum_articles'
		'section_news'
		'section_news_articles'
		'section_outlook'
		'section_outlook_articles'
		'section_sports'
		'section_sports_articles'
		'this_month'
		'this_year'
		'today'
		'top_articles'
		'weekday_header'
		'year'
		'year_minus'
		'year_plus'
	"""
	site = Site.objects.get_current()
	front = WebFront.objects.select_related(depth=1).filter(site=site, type='site').latest()
	
	issue = front.issue
	
	# For the top articles not in the rotation, we choose from published articles that:
	#     * are on the current site,
	#     * were published on or after the day this issue was published and
	#     * don't have publication dates in the future.
	articles = Article.get_published.select_related(depth=1).filter(section__publication__site=site).filter(issue__pub_date__gte=issue.pub_date).filter(issue__pub_date__lte=datetime.now()).order_by('priority')
	
	# Here we get a list of all five top items, for a JavaScript rotation.
	# Note we have two variables with this list — this is due to how our
	# particular rotation is implemented.
	rotating_items = front.item_set.all()
	rotating_item_list = front.item_set.all()

	# Remove the top story from further consideration.
	#B# This will need to be changed to reflect articles no longer being directly FKed to WebFronts.
	#articles = articles.exclude(webfronts__webfront=front)
	
	top_articles = articles[:4]
	
	# Here we get the top five articles from each section.
	
	# NOTE: This hard-codes section names in so that we can control
	# which section appears where in the front page template.
	#B# This will need to be changed to programatically go through sections. We can now order the sections by their ContentChannel's priority.
	
	sections = Section.objects.all().order_by('-priority')[:5]
	section_list = []
	
	for section in sections:
		sec_obj = section
		sec_articles = articles.filter(section=section).order_by('priority')[:5]
		section_dict = {'sec_obj':sec_obj,'articles':sec_articles}
		section_list.append(section_dict)
#    section_news = Section.objects.get(name='News')
#    section_news_articles = articles.filter(section=section_news).order_by('priority')[:5]
#    section_outlook = Section.objects.get(name='Outlook')
#    section_outlook_articles = articles.filter(section=section_outlook).order_by('priority')[:5]
#    section_forum = Section.objects.get(name='Forum')
#    section_forum_articles = articles.filter(section=section_forum).order_by('priority')[:5]
#    section_arts = Section.objects.get(name='Arts')
#    section_arts_articles = section_arts.article_set.filter(published=1).order_by('-pub_date', 'priority')[:5]
#    section_sports = Section.objects.get(name='Sports')
#    section_sports_articles = articles.filter(section=section_sports).order_by('priority')[:5]
	
	# And now we get all blogs that are listed in this publication, and
	# the three most recent posts in these blogs.
	all_blogs = Blog.current.filter(section__publication__site=site).all()
	latest_blog_posts = Entry.get_published.filter(blog__section__publication__site=site)[:3]
	
	# Now we get the latest podcast episodes from across all sites.
	latest_podcast_episodes = Episode.objects.all()[:4]

	# Here we also get the top three online-only stories that:
	#     * aren't published in the future,
	#     * are marked as Web updates and
	#     * aren't in the rotation.
	latest_online_exclusives = Article.get_published.filter(issue__pub_date__lte=datetime.now()).filter(type='online')
#	latest_online_exclusives = latest_online_exclusives.exclude(webfronts__webfront=front)
	latest_online_exclusives = latest_online_exclusives[:3]
	
	# Now to get the most recently released multimedia.
	try:
		latest_video = Video.objects.filter(publication__site=site).latest()
#		latest_video = latest_video.exclude(webfronts__webfront=front).latest()
	except:
		latest_video = ""
	try:
		latest_slideshow = Slideshow.objects.filter(publication__site=site).latest()
#		latest_slideshow = latest_slideshow.exclude(webfronts__webfront=front).latest()
	except:
		latest_slideshow = ""
	try:
		latest_audio = AudioClip.objects.filter(publication__site=site).latest()
#		latest_audio = latest.audio.exclude(webfronts__webfront=front).latest()
	except:
		latest_audio = ""
	
	# Compare the video and slideshow to see which one's newer.
	if latest_slideshow != "" and latest_video != "" and latest_slideshow.pub_date > latest_video.pub_date:
		latest_multimedia = latest_slideshow
	else:
		latest_multimedia = latest_video
	
	# Compare the audio and the winner so far to see which one's newer.
	if latest_audio != "" and latest_multimedia != "" and latest_audio.pub_date > latest_multimedia.pub_date:
		latest_multimedia = latest_audio
	
	# Do we need to show anything else? If so, go ahead and render it.
	#B# Is this still relevant? If so, make it prominent on the page.
	other_info = None
	if front.other_info:
		other_info = markdown(front.other_info)
	
	# Get all events that aren't over and that are in the
	# appropriate calendar.
	events = Event.not_past.filter(calendars=front.calendar)[:5]
	
	# Get all currently-published news bursts.
	#B# Should we have different news bursts for each site?
	news_bursts = NewsBurst.get_published.all()
	
	# Get the front page layout from this issue, if there is one.
	try:
		issue_front = issue.layout_set.filter(type='cover').filter(section__publication__site=site).latest()
	except:
		issue_front = None
	
	# Get all other layouts from this issue.
	issue_other_layouts = issue.layout_set.exclude(type='cover').filter(section__publication__site=site)
	
	# And now, the calendar. Nothing too fancy here; a repaste of the code found in
	# events.views.gridone gets the job done.
	year = datetime.now().year
	month = datetime.now().month
	calendar = None
	calendar_list = Calendar.objects.all().order_by('name')
	events = Event.objects.all()
	month_formatted = pycal.monthcalendar(year, month)
	month_minus = month - 1
	month_plus = month + 1
	month_name = pycal.month_name[month]
	weekday_header = pycal.weekheader(3).strip().split(" ")
	year_minus = year - 1
	year_plus = year + 1
	today = datetime.now().day
	this_month = month
	this_year = year
	event_list = events.filter(Q(start__year=year, start__month=month) | Q(end__year=year, end__month=month))
	
	# A reposting of the method to get events from earlier. Because you just
	# don't want every event THAT WAS EVER PUT IN showing up on the front page.
	events = Event.not_past.filter(calendars=front.calendar)[:5]
	
	#B# Can we do a TopOnline view that can return context here, instead of calling methods ourselves?
	
	page = {
		'all_blogs': all_blogs,
		'calendar': calendar,
		'calendar_list': calendar_list,
		'events': events,
		'event_list': event_list,
		'issue': issue,
		'issue_front': issue_front,
		'issue_other_layouts': issue_other_layouts,
		'latest_audio': latest_audio,
		'latest_blog_posts': latest_blog_posts,
		'latest_multimedia': latest_multimedia,
		'latest_online_exclusives': latest_online_exclusives,
		'latest_podcast_episodes': latest_podcast_episodes,
		'latest_slideshow': latest_slideshow,
		'latest_video': latest_video,
		'month': month,
		'month_formatted': month_formatted,
		'month_minus': month_minus,
		'month_name': month_name,
		'month_plus': month_plus,
		'news_bursts': news_bursts,
		'other_info': other_info,
		'rotating_item_list': rotating_item_list,
		'rotating_items': rotating_items,
		'sections': section_list,
#        'section_arts': section_arts,
#        'section_arts_articles': section_arts_articles,
#        'section_forum': section_forum,
#        'section_forum_articles': section_forum_articles,
#        'section_news': section_news,
#        'section_news_articles': section_news_articles,
#        'section_outlook': section_outlook,
#        'section_outlook_articles': section_outlook_articles,
#        'section_sports': section_sports,
#        'section_sports_articles': section_sports_articles,
		'this_month': this_month,
		'this_year': this_year,
		'today': today,
		'top_articles': top_articles,
		'weekday_header': weekday_header,
		'year': year,
		'year_minus': year_minus,
		'year_plus': year_plus,
	}
	
	return render_to_response('frontpage/frontpage.html', page, context_instance=RequestContext(request))

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
		lead_item = section_front.item_set.all()[:1]
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

# @cache_page(60 * 5)
# def top_online(request):

	# connection = Connection(settings.ANALYTICS_EMAIL_ADDRESS, settings.ANALYTICS_EMAIL_PASSWORD)

	# account = connection.get_accounts()[0]

#    today = datetime.today()

#    issues = Issue.objects.all().order_by('-pub_date').filter(online_update=0).filter(pub_date__lte=today)

# start = issues[1].pub_date.date()

# end = issues[0].pub_date.date()-timedelta(days=1)

#    start = issues[0].pub_date.date()

#    end = date.today()

# top_hits = account.get_data(start_date=start, end_date=end, dimensions=['pagePath',], metrics=['pageviews',], sort=['-pageviews',])

# top_hits_list = top_hits.tuple[:25]

# top_pages = account.get_data(start_date=start, end_date=end, dimensions=['pageTitle','pagePath',], metrics=['pageviews',], sort=['-pageviews',])

	# top_pages_list = top_pages.tuple[:25]

# allowed_url_bases = ['audio', 'blogs', 'calendar', 'graphics', 'layouts', 'maps', 'photos', 'podcasts', 'polls', 'slideshows', 'stories', 'videos']

	# top_content = []
	# for entry in top_hits_list:
		# substring = entry[0][0].split('/')
		# if substring[1] in allowed_url_bases:
			# top_content.append((entry, substring[1]))

	# top_online = []
	# for entry in top_content:
		# if entry[1] == 'audio':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# audioclip = AudioClip.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(audioclip)
			# except:
				# pass
		# elif entry[1] == 'blogs':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[3]
				# month = substring[4]
				# day = substring[5]
				# slug = substring[6]
				# entry = Entry.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(slug=slug)
				# top_online.append(entry)
			# except:
				# pass
		# elif entry[1] == 'calendar':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# slug = substring[5]
				# event = Event.objects.filter(start__year=year).filter(start__month=month).filter(start__day=day).get(slug=slug)
				# top_online.append(event)
			# except:
				# pass
		# elif entry[1] == 'graphics':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# graphic = Graphic.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(graphic)
			# except:
				# pass
		# elif entry[1] == 'layouts':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# layout = Layout.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(layout)
			# except:
				# pass
		# elif entry[1] == 'maps':
			# try:
				# substring = entry[0][0][0].split('/')
				# slug = substring[2]
				# map = Poll.objects.get(slug=slug)
				# top_online.append(map)
			# except:
				# pass
		# elif entry[1] == 'photos':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# photo = Photo.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(photo)
			# except:
				# pass
		# elif entry[1] == 'podcasts':
			# try:
				# substring = entry[0][0][0].split('/')
				# id = substring[3]
				# episode = Episode.objects.get(id=id)
				# top_online.append(episode)
			# except:
				# pass
		# elif entry[1] == 'polls':
			# try:
				# substring = entry[0][0][0].split('/')
				# id = substring[2]
				# poll = Poll.objects.get(id=id)
				# top_online.append(poll)
			# except:
				# pass
		# elif entry[1] == 'slideshows':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# slideshow = Slideshow.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(slideshow)
			# except:
				# pass
		# elif entry[1] == 'stories':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# slug = substring[5]
				# article = Article.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(slug=slug)
				# top_online.append(article)
			# except:
				# pass
		# elif entry[1] == 'videos':
			# try:
				# substring = entry[0][0][0].split('/')
				# year = substring[2]
				# month = substring[3]
				# day = substring[4]
				# id = substring[5]
				# video = Video.objects.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).get(id=id)
				# top_online.append(video)
			# except:
				# pass
				
	# top_online = top_online[:10]

	# page = {
		# 'end': end,
		# 'start': start,
		# 'top_content': top_content,
		# 'top_hits_list': top_hits_list,
		# 'top_online': top_online,
		# 'top_pages_list': top_pages_list,
	# }

	# return render_to_response('management/top_online.html', page, context_instance=RequestContext(request))