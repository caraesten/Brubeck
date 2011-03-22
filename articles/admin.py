from brubeck.articles.models import *
from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment

from brubeck.core.models import Content

admin.site.register(Article)
