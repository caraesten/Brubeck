# Imports from Django
from django.contrib import admin

# Imports from brubeck
from brubeck.reporters.models import *

class SourceTypeAdmin(admin.ModelAdmin):
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
    admin.site.register(SourceType, SourceTypeAdmin)
except admin.sites.AlreadyRegistered:
    pass

class AddressInline(admin.TabularInline):
    model = Address
    extra = 3
class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 3

class SourceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('prefix', 'first_name', 'last_name'), 'position', 'org')
        }),
        ("Details", {
            'fields': ('email', 'other_info', 'mugshot', 'types')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    inlines = [
        AddressInline,
        PhoneNumberInline
    ]
    list_display = ('last_name', 'first_name', 'org', 'position')
    prepopulated_fields = {
        'slug': ('first_name', 'last_name')
    }
    search_fields = ['id', 'first_name', 'last_name', 'position', 'org', 'email', 'other_info',]
    search_fields_verbose = ['ID', 'first name', 'last name', 'position', 'organization', 'e-mail address', 'other info',]

try:
    admin.site.register(Source, SourceAdmin)
except admin.sites.AlreadyRegistered:
    pass

class InfoPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'body')
        }),
        ("Don't touch unless you know what you're doing", {
            'classes': ('collapse closed',),
            'fields': ('slug',)
        }),
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ['id', 'title', 'description', 'body',]
    search_fields_verbose = ['ID', 'title', 'description', 'body',]

try:
    admin.site.register(InfoPage, InfoPageAdmin)
except admin.sites.AlreadyRegistered:
    pass

