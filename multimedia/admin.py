"""Multimedia admin

Provide administrative functionality for the multimedia module.

"""

# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.multimedia.models import *

class AttachedFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_filter = ['pub_date']
    list_display = ('title', 'pub_date', 'file',)
    search_fields = ['id', 'title', 'pub_date', 'description']
    search_fields_verbose = ['ID', 'title', 'publication date', 'description',]
try:
    admin.site.register(AttachedFile, AttachedFileAdmin)
except admin.sites.AlreadyRegistered:
    pass

class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'byline', 'static_byline')
        }),
        ("Publication information", {
            'fields': ('pub_date', 'publication')
        }),
        ("The video", {
            'fields': ('url', 'length', 'description')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('enable_comments', 'thumbnail', 'preview_image', 'swf')
        }),
    )
    filter_horizontal = ['byline']
    list_filter = ['pub_date']
    search_fields = ['id', 'title', 'pub_date', 'description',]
    search_fields_verbose = ['ID', 'title', 'publication date', 'description',]
    list_display = ('title', 'pub_date', 'length',)

try:
    admin.site.register(Video, VideoAdmin)
except admin.sites.AlreadyRegistered:
    pass

class SlideshowAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'byline', 'static_byline', 'publication', 'pub_date', 'description', 'length', 'image', 'zip')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('enable_comments', 'swf',)
        }),
    )
    filter_horizontal = ['byline',]
    list_filter = ['publication', 'pub_date']
    search_fields = ['id', 'title', 'pub_date', 'description',]
    search_fields_verbose = ['ID', 'title', 'publication date', 'description',]
    list_display = ('title', 'pub_date', 'publication', 'length',)

try:
    admin.site.register(Slideshow, SlideshowAdmin)
except admin.sites.AlreadyRegistered:
    pass

class AudioClipAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'pub_date', 'publication', 'description', 'length')
        }),
        ("Files", {
            'fields': ('audio_file', 'image')
        }),
        ("Attribution", {
            'fields': ('byline', 'static_byline',)
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('enable_comments',),
        }),
    )
    filter_horizontal = ['byline']
    list_filter = ['pub_date']
    search_fields = ['id', 'title', 'pub_date', 'description',]
    search_fields_verbose = ['ID', 'title', 'publication date', 'description',]
    list_display = ('title', 'pub_date', 'length',)
try:
    admin.site.register(AudioClip, AudioClipAdmin)
except admin.sites.AlreadyRegistered:
    pass
