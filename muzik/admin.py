# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Artist, Album, Tag, Song

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Tag)
admin.site.register(Song)
