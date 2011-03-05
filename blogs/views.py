# Imports from standard libraries
from datetime import date, datetime
import calendar as pycal

# Imports from Django
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.dateformat import format
from django.utils.html import urlize
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_day, archive_month, archive_year
from django.core.paginator import EmptyPage, InvalidPage, Paginator

# Imports from brubeck
from brubeck.blogs.models import Blog, Entry

def blog_index(request, blog_slug=None, page='1'):
    """
    Displays a paginated list of all entries for a given blog by wrapping the 
    generic object_list view. The date-based archive_index view only listed the
    latest n entries, which wasn't the behavior we were after. (The pagination
    just works so much better.)
    """
    blog = get_object_or_404(Blog, slug=blog_slug)
    entries = Entry.get_published.filter(blog=blog)
    archive_name = "Latest entries in %s" % blog
    return object_list(request, entries, paginate_by=10, page=page, extra_context={'blog': blog, 'archive_name': archive_name}, allow_empty=True, template_name='blogs/entry_archive.html')

def blog_date(request, blog_slug=None, year=None, month=None, day=None):
    """
    Shows all of a blog's entries for a given day, month or year using the 
    appropriate generic view.
    """
    blog = Blog.objects.get(slug=blog_slug)
    entries = Entry.get_published.filter(blog=blog)
    if day:
        date_string = format(date(int(year), int(month), int(day)), "N j, Y")
        archive_name = "Posts to %s on %s" % (blog, date_string)
        return archive_day(request, year, month, day, entries, 'pub_date', month_format='%m', extra_context={'blog': blog, 'archive_name': archive_name}, allow_empty=True, template_name='blogs/entry_archive.html')
    elif month:
        date_string = format(date(int(year), int(month), 1), "F Y")
        archive_name = "Posts to %s in %s" % (blog, date_string)
        return archive_month(request, year, month, entries, 'pub_date', month_format='%m', extra_context={'blog': blog, 'archive_name': archive_name}, allow_empty=True, template_name='blogs/entry_archive.html')
    elif year:
        archive_name = "Months in %s with posts to %s" % (year, blog)
        return archive_year(request, year, entries, 'pub_date', extra_context={'blog': blog, 'archive_name': archive_name}, allow_empty=True, template_name='blogs/entry_archive.html')

def blog_entry(request, blog_slug=None, year=None, month=None, day=None, slug=None, mode=None):
    """
    Shows a specific blog entry, including any attached photos.
    """
    try:
        blog = Blog.objects.get(slug=blog_slug)
    except Blog.DoesNotExist:
        raise Http404
    
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except ValueError:
        raise Http404
    
    try:
        entry = Entry.get_published.filter(blog=blog)
        entry = entry.filter(pub_date__year=year, pub_date__month=month, pub_date__day=day)
        entry = entry.get(slug=slug)
    except Entry.DoesNotExist:
        raise Http404
    
    images = []
    images.extend(entry.photos.all())

    multimedia = []
    multimedia.extend(entry.videos.all())
    multimedia.extend(entry.slideshows.all())
    multimedia.extend(entry.audio_clips.all())

    entry.attached_audio = False
    for item in entry.attached_files.all():
        if item.get_file_extension() == 'mp3':
            entry.attached_audio = True
    
    page = {
        'blog': blog,
        'entry': entry,
        'images': images,
        'multimedia': multimedia,
    }
    
    if mode == 'images':
        return render_to_response('blogs/entry_detail_images.html', page, context_instance=RequestContext(request))
    else:
        return render_to_response('blogs/entry_detail.html', page, context_instance=RequestContext(request))

def list_blogs(request, archive=False):
    """
    Shows all current blogs and any active live blogs. If the user requests an archive instead, show absolutely everything.
    """
    site = Site.objects.get_current()
    current = Blog.current.filter(section__publication__site=site).all()
    current_entries = Entry.get_published.filter(blog__section__publication__site=site).filter(blog__in=current)[:5]
    if archive:
        live_blogs = Blog.live_blogs.filter(section__publication__site=site)
        live_blogs_entries = Entry.get_published.filter(blog__section__publication__site=site).filter(blog__in=live_blogs)[:5]
        live_blog_ids = []
        for blog in live_blogs:
            live_blog_ids.append(blog.id)
        archived = Blog.old.filter(section__publication__site=site).exclude(id__in=live_blog_ids)
    else:
        archived = None
        archived_entries = None
        live_blogs = Blog.active_live_blogs.filter(section__publication__site=site)
        live_blogs_entries = Entry.get_published.filter(blog__section__publication__site=site).filter(blog__in=live_blogs)[:5]
    
    page = {
        'archive': archive,
        'archived': archived,
        'current': current,
        'current_entries': current_entries,
        'live_blogs': live_blogs,
        'live_blogs_entries': live_blogs_entries,
    }
    
    return render_to_response('blogs/front.html', page, context_instance=RequestContext(request))
    
def calendar_view(request, year=datetime.now().year, month=datetime.now().month, blog_slug=None, page=1):
    """
    Shows a grid (similar in appearance to a physical calendar) of blogs for either entries in a specific blog or all entries.  Based on the GridOne layout originally developed for Calendars.
    """
    site = Site.objects.get_current()
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
    except ValueError:
        raise Http404

    blog = None
    blog_list = Blog.current.filter(section__publication__site=site).order_by('title')
    entries = Entry.get_published.filter(blog__section__publication__site=site)
    if blog_slug:
        blog = get_object_or_404(Blog, slug=blog_slug)
        entries = entries.filter(blog=blog)

    month_formatted = pycal.monthcalendar(year, month)

    month_minus = month - 1

    month_plus = month + 1

    month_name = pycal.month_name[month]

    weekday_header = pycal.weekheader(3).strip().split(" ")                                              

    year_minus = year - 1

    year_plus = year + 1

    today = datetime.now().day

    this_month = datetime.now().month

    this_year = datetime.now().year

    entry_list = entries.filter(pub_date__year=year).filter(pub_date__month=month)
    page_name = "This is a test of the calendaring system."

    page = {
        'blog': blog,
        'blog_list': blog_list,
        'entry_list': entry_list,
        'month': month,
        'month_formatted': month_formatted,
        'month_minus': month_minus,
        'month_name': month_name,
        'month_plus': month_plus,
        'page_name': page_name,
        'site': site,
        'this_month': this_month,
        'this_year': this_year,
        'today': today,
        'weekday_header': weekday_header,
        'year': year,
        'year_minus': year_minus,
        'year_plus': year_plus,
    }

    return render_to_response('blogs/calendar.html', page, context_instance=RequestContext(request))



def calendar_day_view(request, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, blog_slug=None, page=1):
    """
    Shows a grid (similar in appearance to a physical calendar) of blogs for either entries in a specific blog or all entries.  Based on the GridOne layout originally developed for Calendars.
    """
    site = Site.objects.get_current()
    try:
        page = int(page)
        if year:
            year = int(year)
        if month:
            month = int(month)
    except ValueError:
        raise Http404

    blog = None
    blog_list = Blog.current.filter(section__publication__site=site).order_by('title')
    entries = Entry.get_published.filter(blog__section__publication__site=site)
    if blog_slug:
        blog = get_object_or_404(Blog, slug=blog_slug)
        entries = entries.filter(blog=blog)

    month_formatted = pycal.monthcalendar(year, month)

    month_minus = month - 1

    month_plus = month + 1

    month_name = pycal.month_name[month]

    weekday_header = pycal.weekheader(3).strip().split(" ")                                              

    year_minus = year - 1

    year_plus = year + 1

    today = datetime.now().day

    this_month = datetime.now().month

    this_year = datetime.now().year

    entry_list = entries.filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day).order_by('pub_date')
    page_name = "This is a test of the calendaring system."

    page = {
        'blog': blog,
        'blog_list': blog_list,
        'day': day,
        'entry_list': entry_list,
        'month': month,
        'month_formatted': month_formatted,
        'month_minus': month_minus,
        'month_name': month_name,
        'month_plus': month_plus,
        'page_name': page_name,
        'site': site,
        'this_month': this_month,
        'this_year': this_year,
        'today': today,
        'weekday_header': weekday_header,
        'year': year,
        'year_minus': year_minus,
        'year_plus': year_plus,
    }

    return render_to_response('blogs/calendarday.html', page, context_instance=RequestContext(request))
