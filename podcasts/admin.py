# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.podcasts.models import *

class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'section', 'keywords', 'archived')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    filter_horizontal = ['section']
    list_filter = ['archived', 'section']
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ['id', 'title', 'description', 'keywords',]
    search_fields_verbose = ['ID', 'title', 'description', 'keywords',]

try:
    admin.site.register(Channel, ChannelAdmin)
except admin.sites.AlreadyRegistered:
    pass

class EpisodeAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('channel', 'pub_date', 'name')
        }),
        ("Content", {
            'fields': ('file', 'description', 'keywords')
        }),
        ("Credits", {
            'fields': ('producers', 'writers', 'reporters')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('enable_comments',)
        }),
    )
    filter_horizontal = ['producers', 'writers', 'reporters']
    list_filter = ['channel']
    search_fields = ['id', 'name', 'pub_date', 'description', 'keywords',]
    search_fields_verbose = ['ID', 'descriptive name', 'publication date', 'description', 'keywords',]

try:
    admin.site.register(Episode, EpisodeAdmin)
except admin.sites.AlreadyRegistered:
    pass

