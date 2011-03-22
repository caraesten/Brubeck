# Imports from Django
from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment

# Imports from brubeck
from brubeck.blogs.models import *
from brubeck.core.models import Content

class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name','description')
        }),
        ("Publication information", {
            'fields': ('section', 'is_live_blog', 'is_archived')
        }),
        ("Moderators", {
            'fields': ('editorial_moderators', 'staff_moderators', 'moderators')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    filter_horizontal = ['editorial_moderators', 'staff_moderators']
    list_display = ('name', 'section', 'is_archived', 'is_live_blog')
    list_filter = ['is_archived', 'is_live_blog']
    prepopulated_fields = {
        'slug': ('name',)
    }
    search_fields = ['id', 'name', 'description',]
    search_fields_verbose = ['ID', 'title', 'description',]

try:
    admin.site.register(Blog, BlogAdmin)
except admin.sites.AlreadyRegistered:
    pass
    
class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'pub_date', 'blog', 'is_published', 'byline', 'static_byline')
        }),
        ("Content", {
            'fields': ('body', 'photos', 'tags')
        }),
	("Attached multimedia", {
            'classes': ('collapse closed',),
            'fields': ('attached_files', 'videos', 'slideshows', 'audio_clips',),
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('enable_comments', 'slug')
        }),
    )
    filter_horizontal = ['photos', 'tags']
    list_display = ('title', 'blog', 'pub_date', 'is_published')
    list_editable = ('is_published',)
    list_filter = ['blog']
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ['id', 'title', 'pub_date', 'body']
    search_fields_verbose = ['ID', 'title', 'publication date', 'body']

try:
    admin.site.register(Entry, EntryAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Change the way comments display in the admin site.
# See http://justinlilly.com/blog/2009/feb/10/better-look-comments/ for details.

admin.site.unregister(Comment)
class CommentsDisplayGenericObjectAdmin(CommentsAdmin):
    list_display = ('name', 'commented_object', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    
    def commented_object(self, obj):
        return '<a href="%s">%s</a>' % (self.commented_obj_url(obj.content_object), obj.content_object)
    commented_object.allow_tags = True
    
    def commented_obj_url(self, obj):
        return '/admin/%s/%s/%s/' % (obj._meta.app_label, obj._meta.module_name, obj.id)
admin.site.register(Comment, CommentsDisplayGenericObjectAdmin)
