# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.comics.models import *

class ComicStripAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'volume', 'is_archived')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    prepopulated_fields = {
        'slug': ('name', 'volume')
    }
    search_fields = ['id', 'name',]
    search_fields_verbose = ['ID', 'title',]

try:
    admin.site.register(ComicStrip, ComicStripAdmin)
except admin.sites.AlreadyRegistered:
    pass

class ComicEpisodeAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('__unicode__', 'issue')
    list_filter = ['strip']
    search_fields = ['id', 'pub_date',]
    search_fields_verbose = ['ID', 'publication date',]

try:
    admin.site.register(ComicEpisode, ComicEpisodeAdmin)
except admin.sites.AlreadyRegistered:
    pass
