# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.advertising.models import *

# Advertising information
class AdditionalLinkInline(admin.TabularInline):
    model = AdditionalLink
    num = 5

class InfoPageAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    fieldsets = (
        (None, {
            'fields': ('rate_card',)
        }),
        ("Credit applications", {
            'fields': ('io_app', 'credit_app')
        }),
        ("Contracts", {
            'fields': ('contract', 'back_cover_contract')
        }),
    )
    inlines = [
        AdditionalLinkInline
    ]

try:
    admin.site.register(InfoPage, InfoPageAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Banner ads and such
class BannerAdAdmin(admin.ModelAdmin):
    date_hierarchy = 'end_date'
    fieldsets = (
        (None, {
            'fields': ('name', 'start_date', 'end_date')
        }),
        ("Publishing information", {
            'fields': ('ad_type', 'site', 'special_section')
        }),
        ("Image-based ad", {
            'fields': ('image', 'url')
        }),
        ("Code-based ad", {
            'classes': ('collapse closed',),
            'fields': ('code',)
        }),
    )
    list_display = ('name', 'start_date', 'end_date', 'ad_type', 'site')
    list_filter = ['start_date', 'end_date', 'site']

try:
    admin.site.register(BannerAd, BannerAdAdmin)
except admin.sites.AlreadyRegistered:
    pass

