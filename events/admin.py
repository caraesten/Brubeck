# Imports from Django
from django.contrib import admin

# Imports from maneaer
from brubeck.events.models import *

class CalendarAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name','priority')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    prepopulated_fields = {
        'slug': ('name',)
    }
    search_fields = ['id', 'name',]
    search_fields_verbose = ['ID', 'name',]
try:
    admin.site.register(Calendar, CalendarAdmin)
except admin.sites.AlreadyRegistered:
    pass

class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    fieldsets = (
        (None, {
            'fields': ('name', 'summary', 'description', 'calendars')
        }),
        ("When and where", {
            'fields': ('start', 'end', 'all_day', 'location')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    filter_horizontal = ['calendars']
    list_display = ('name', 'start', 'end', 'location')
    list_filter = ['start', 'end']
    # prepopulated_fields = {
    #     'slug': ('name',)
    # }
    search_fields = ['id', 'name', 'summary', 'description',]
    search_fields_verbose = ['ID', 'name', 'summary', 'description',]
try:
    admin.site.register(Event, EventAdmin)
except admin.sites.AlreadyRegistered:
    pass

