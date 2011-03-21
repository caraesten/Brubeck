# Imports from standard libraries
from datetime import date, datetime, time

# Imports from Django
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.template.defaultfilters import escape

# Import from maneater
from brubeck.articles.models import Article
from brubeck.blogs.models import Entry
from brubeck.tagging.models import Tag

def list_authors(item):
    """
    Lists any staff members in the byline according to AP list style. Falls
    back to the static byline and then simply to a staff credit.
    """
    authors = ''
    byline = item.byline.all()
    if byline:
        staffers = byline.count()
        counter = 1
        for staffer in byline:
            if counter != 1:
                if counter == staffers:
                    authors += ' and '
                else:
                    authors += ', '
            authors += escape(staffer)
            counter += 1
    elif item.static_byline:
        authors = item.static_byline
    else:
        authors = 'The Maneater Staff'
    return authors

class TagFeed(Feed):
    """
    Lists the latest articles and blog posts with a certain tag.
    """
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(slug=bits[0])

    def title(self, obj):
        return "The Maneater - %s" % obj.title

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return '/feeds/tags/%s/' % obj.slug

    def description(self, obj):
        return "The latest articles about %s from themaneater.com." % obj.title

    author_name = "The Maneater"
    author_email = 'online@themaneater.com'
    categories = ('news', 'college', 'university', 'student news', 'student newspaper', 'missouri', 'mizzou', 'university of missouri', 'maneater')
    copyright = "Copyright &xa9; %s The Maneater Student Newspaper" % date.today().year

    def items(self, obj):
        articles = Article.get_published.filter(tags=obj)[:30]
        entries = Entry.get_published.filter(tags=obj)[:30]

        all_content = []

        for article in articles:
            all_content.append((article.pub_date, article))

        for entry in entries:
            all_content.append((entry.pub_date.date(), entry))

        sorted_content = sorted(all_content, key=lambda item: item[0])
        sorted_content.reverse()

        item_list = []
        for content in sorted_content:
            item_list.append(content[1])

        return item_list

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        if item.mediatype == 'article':
            return list_authors(item)
        elif item.mediatype == 'blog':
            if item.byline:
                return item.byline
            elif item.static_byline:
                return item.static_byline
            else:
                return 'The Maneater staff'

    def item_pubdate(self, item):
        if item.mediatype == 'article':
            return datetime.combine(item.pub_date, time.min)
        elif item.mediatype == 'blog':
            return item.pub_date

    def item_copyright(self, item):
        return "Copyright &xa9; %s The Maneater Student Newspaper" % item.pub_date.year