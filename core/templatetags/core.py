# Imports from standard libraries
from datetime import datetime
import operator

# Imports from other dependencies
import markdown
#     mailhide requires pycrypto
from recaptcha.client import mailhide
import tweepy
import twitter

# Imports from Django
from django import template
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

# Imports from maneater
from brubeck.blogs.models import Entry
from brubeck.articles.models import Article
from brubeck.publishing.models import Issue
from brubeck.photography.models import Photo
from brubeck.tagging.models import Tag
from brubeck.management.models import WebFront
from brubeck.voxpopuli.models import Poll
#from brubeck.socialmedia.models import TwitterAccount

register = template.Library()

@register.simple_tag
def render_flatpage(url):
    """
    Outputs the content of a flatpage to be inserted into a template. Handy for
    providing little places throughout the site that are relatively easy for
    other editors to change. (The main one of these is below the ticker and
    search, on the right side of the bar with the publication flag.)
    """
    site = Site.objects.get_current()
    try:
        flatpage = FlatPage.objects.filter(sites=site).get(url=url)
    except FlatPage.DoesNotExist:
        return ''
    if flatpage.content == '':
        return ''
    else:
        return flatpage.content

@register.simple_tag
def render_flatpage_with_markdown(url):
    """
    Outputs the content of a flatpage to be inserted into a template. Handy for
    providing little places throughout the site that are relatively easy for
    other editors to change. (The main one of these is below the ticker and
    search, on the right side of the bar with the publication flag.)
    """
    site = Site.objects.get_current()
    try:
        flatpage = FlatPage.objects.filter(sites=site).get(url=url)
    except FlatPage.DoesNotExist:
        return ''
    if flatpage.content == '':
        return ''
    else:
        return markdown.markdown(flatpage.content)



@register.inclusion_tag('core/ticker.html')
def render_ticker():
    """
    This pulls the latest 10 articles from the current site that have been
    published since the latest issue (and aren't in the Forum section).
    As you can imagine, this is a little database-intensive; nothing crazy, but
    certainly not something I'd like to be running with every single pageview.
    Caching is definitely recommended here.
    """
    site = Site.objects.get_current()
    
    cache_name = 'ticker-maneater'
    articles = cache.get(cache_name)
    
    if not articles:
        try:
            issue = Issue.objects.filter(volume__publication__site=site).filter(pub_date__lte=datetime.now()).filter(online_update=False).latest()
            articles = Article.get_published.filter(section__publication__site=site).filter(issue__pub_date__gte=issue.pub_date).filter(issue__pub_date__lte=datetime.now()).exclude(section__slug='forum')[:10]
            cache.set(cache_name, articles, 60 * 10)
        except:
            articles = None
    
    return {
        'articles': articles
    }

# @register.inclusion_tag('core/twitter_list.html')
# def render_tweets(limit=None):
#     """
#     Pulls the latest five tweets from each of Brubeck's Twitter
#     accounts and sorts them by the date they were posted, from newest to
#     oldest.
#     """
# 
#     cache_name = 'compiled-tweets'
#     tweet_list = cache.get(cache_name)
# 
#     if not tweet_list:
#         try:
#             """
#             Try to import the Twitter accounts listed in settings.
#             """
#             default_twitter_account_id = settings.DEFAULT_TWITTER_ACCOUNT_ID
#             default_twitter_list = settings.DEFAULT_TWITTER_LIST
#             twitter_accounts = settings.TWITTER_ACCOUNTS
#         except:
#             """
#             If there are no Twitter accounts in settings, just use the
#             default account.
#             """
#             default_twitter_account_id = '8'
#             default_twitter_list = 'maneater-twitter-accounts'
# 
#         try:
#             auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
#             default_user = TwitterAccount.objects.get(id=default_twitter_account_id)
#             auth.set_access_token(default_user.access_key, default_user.access_secret)
#             api = tweepy.API(auth)
# 
#            twitter_api = twitter.Api(username=settings.TWITTER_ACCOUNTS[0][0], password=settings.TWITTER_ACCOUNTS[0][1])
#            unordered_tweets = []
#            for account in twitter_accounts:
#                unordered_tweets.extend(twitter_api.GetUserTimeline(account[0])[:5])
#            tweet_times = []
#            for tweet in unordered_tweets:
#                tweet_times.append((tweet.created_at_in_seconds, tweet))
#            map(operator.itemgetter(0), tweet_times)
#            ordered_tweets = sorted(tweet_times,key=operator.itemgetter(0), reverse=True)
#            tweet_list = []
#            for tweet in ordered_tweets:
#                tweet_list.append(tweet[1])
#             tweet_list = api.list_timeline(owner=api.me().screen_name, slug=default_twitter_list, per_page=limit)
#             cache.set(cache_name, tweet_list, 60 * 10)
#         except:
#             tweet_list = None
# 
#     if limit:
#         try:
#             limit = int(limit)
#             tweet_list = tweet_list[:limit]
#         except:
#             pass
# 
#     return {
#         'tweet_list': tweet_list
#     }
# 
# @register.inclusion_tag('core/twitter_list_by_account.html')
# def render_tweets_by_account(account='themaneater', limit=None):
#     """
#     Pulls the latest ten tweets from the given Twitter account
#     and sorts them by the date they were posted, from newest to
#     oldest.
#     """
#     
#     cache_name = 'compiled-tweets-by-account-%s' % account
#     tweet_list = cache.get(cache_name)
#     
#     if not tweet_list:
#         try:
#             """
#             Try to import the Twitter accounts listed in settings.
#             """
#             all_accounts = settings.TWITTER_ACCOUNTS
#         except:
#             """
#             If there are no Twitter accounts in settings, just use the
#             default account.
#             """
#             all_accounts = (
#                 ('themaneater', 'hoochfest'),
#             )
# 
#         twitter_account = account
#         twitter_password = None
# 
#         for account in all_accounts:
#             if account[0] == twitter_account:
#                 twitter_password = account[1]
# 
# 	try:
#             twitter_api = twitter.Api(username=twitter_account, password=twitter_password)
#             tweet_list = twitter_api.GetUserTimeline(twitter_account)[:10]
#             cache.set(cache_name, tweet_list, 60 * 10)
#         except:
#             tweet_list = None
# 
#     if limit:
# 	try:
#             limit = int(limit)
#             tweet_list = tweet_list[:limit]
#         except:
#             pass
# 
#     return {
# 	'tweet_list': tweet_list
#     }

@register.filter
@stringfilter
def twitterize(value, autoescape=None):
	from django.utils.html import urlize
	import re
	# Link URLs
	value = urlize(value, nofollow=False, autoescape=autoescape)
	# Link twitter usernames prefixed with @
	value = re.sub(r'(\s+|\A)@([a-zA-Z0-9\-_]*)\b',r'\1<a class="atreply" href="http://twitter.com/\2">@\2</a>',value)
	# Link hash tags
	value = re.sub(r'(\s+|\A)#([a-zA-Z0-9\-_]*)\b',r'\1<a class="hashtag" href="http://search.twitter.com/search?q=%23\2">#\2</a>',value)
	return mark_safe(value)
twitterize.is_safe=True
twitterize.needs_autoescape = True


@register.filter
def mailhide(value):
    """
    Turns an e-mail address into a reCAPTCHA MailHide link.
    """
    link = mailhide.ashtml(value, settings.MAILHIDE_PUBLIC_KEY, settings.MAILHIDE_PRIVATE_KEY)
    return mark_safe(link)

@register.filter
def truncate_paragraphs(value, arg):
    try:
        length = int(arg)
    except ValueError:
        return value
    paragraphs = value.split('</p>\n')
    # Sometimes we end up somehow separating them with carriage returns instead
    # of newlines. This checks to see if the first split actually did anything
    # and makes a second attempt if it didn't.
    if paragraphs == [value]:
        paragraphs = value.split('</p>\r')
    if len(paragraphs) > length:
        paragraphs = paragraphs[:length]
    truncated = '</p>\n'.join(paragraphs)
    truncated += '</p>'
    return truncated
truncate_paragraphs.is_safe = True

@register.filter
def columns(thelist, n):
    """
    Break a list into n columns, filling up each column to the maximum equal
    length possible.
    
    Taken from http://www.djangosnippets.org/snippets/401/
    
    Usage:
        {% for row in mylist|columns:3 %}
            <tr>
                {% for item in row %}
                <td>{{ item }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    list_len = len(thelist)
    split = list_len // n
    if list_len % n != 0:
        split += 1
    return [thelist[i::split] for i in range(split)]

@register.inclusion_tag('core/sidebar_object_list.html')
def show_related_articles(object):
    try:
        list_name = "Related articles"
        objects = Article.get_published.filter(tags__in=object.tags.all()).distinct()
        if isinstance(object, Article):
            objects = objects.exclude(id=object.id)
        objects = objects[:5]
        return {
            'list_name': list_name,
            'objects': objects
        }
    except:
        return ''

@register.inclusion_tag('core/sidebar_object_list.html')
def show_related_blog_posts(object):
    try:
        list_name = "Related blog posts"
        objects = Entry.get_published.filter(tags__in=object.tags.all()).distinct()[:5]
        if isinstance(object, Entry):
            objects = objects.exclude(id=object.id)
        objects = objects[:5]
        return {
            'list_name': list_name,
            'objects': objects
        }
    except:
        return ''

@register.inclusion_tag('core/disclaimer.html')
def show_disclaimer(article):
    try:
        type = article.type
        return {
            'type': type,
        }
    except:
        return ''

@register.inclusion_tag('core/disclaimer_archive.html')
def show_disclaimer_archive():
    return ''

@register.inclusion_tag('core/top_editorial_cartoon.html')
def render_top_editorial_cartoon():

    site = Site.objects.get_current()
        
    front = WebFront.objects.select_related(depth=1).filter(site=site, type='site').latest()

    issue = front.issue
        
    latest_cartoons = issue.editorialcartoon_set.all()
        
    try:
        try:
            latest_cartoon = latest_cartoons.filter(article__isnull=True)[0]
        except:
            latest_cartoon = latest_cartoons[0]
    except:
        latest_cartoon = None

    try:
        return {
            'latest_cartoon': latest_cartoon,
        }
    except:
        return ''

@register.inclusion_tag('core/editorial_cartoon_sidebar.html')
def render_editorial_cartoon_sidebar():

    site = Site.objects.get_current()

    front = WebFront.objects.select_related(depth=1).filter(site=site, type='site').latest()

    issue = front.issue

    latest_cartoons = issue.editorialcartoon_set.all()

    try:
        try:
            latest_cartoon = latest_cartoons.filter(article__isnull=True)[0]
        except:
            latest_cartoon = latest_cartoons[0]
    except:
        latest_cartoon = None

    try:
        return {
            'latest_cartoon': latest_cartoon,
        }
    except:
        return ''

@register.inclusion_tag('core/gallery_setup.html')
def gallery_setup(gallery_id, size="large"):
    try:
        return {
            'gallery_id': gallery_id,
            'size': size
        }
    except:
        return ''

@register.inclusion_tag('core/render_byline.html')
def render_byline(byline_field):
    try:
        return {
            'byline': byline_field
        }
    except:
        return ''


@register.inclusion_tag('core/render_photos_by_tag.html')
def render_photos_by_tag(tag_id, num_photos):

    try:
        tag_id = int(tag_id)
    except:
        tag_id = None

    try:
        num_photos = int(num_photos)
    except:
        num_photos = None

    chosen_tag = Tag.objects.get(id=tag_id)

    photos = Photo.objects.filter(tags=chosen_tag)

    if num_photos:
        photo_subset = photos[:num_photos]
    else:
        photo_subset = photos

    return {
        'photo_subset': photo_subset,
    }

@register.inclusion_tag('core/question_form.html')
def render_latest_question():
    """
    Retrieves the latest question. Used to render a
    response form for Question of the Week on section heads.
    """
    question = Poll.objects.latest()

    return {
        'question': question,
    }

@register.inclusion_tag('core/articles/render_article.html')
def render_article(article_id):
    """
    Shows a particular article or its associated photos and graphics.
    """
    site = Site.objects.get_current()
    try:
        article = Article.get_published.filter(section__publication__site=site).get(id=article_id)
    except Article.DoesNotExist:
        return 'Error retrieving article.'

    images = []
    images.extend(article.photos.all())
    images.extend(article.editorial_cartoons.all())
    images.extend(article.graphics.all())

    multimedia = []
    multimedia.extend(article.videos.all())
    multimedia.extend(article.slideshows.all())
    multimedia.extend(article.audio_clips.all())
    multimedia.extend(article.podcast_episodes.all())

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

    return {
	'article': article,
        'images': images,
        'multimedia': multimedia
    }
