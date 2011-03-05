"""
Provides administrative functionality to the games module.
"""

# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.games.models import *

class GameTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',)
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
    admin.site.register(GameType, GameTypeAdmin)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(GameAnswer)
except admin.sites.AlreadyRegistered:
    pass
