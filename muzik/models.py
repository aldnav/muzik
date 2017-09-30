# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=254)
    gender = models.CharField(max_length=7, blank=True)
    disambiguation = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    area = models.CharField(max_length=64, blank=True)
    play_count = models.IntegerField(null=True, blank=True)
    listener_count = models.IntegerField(null=True, blank=True)


class Album(models.Model):
    title = models.CharField(max_length=254)
    release_date = models.DateField(null=True, blank=True)
    play_count = models.IntegerField(null=True, blank=True)
    listener_count = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=64, blank=True)
    label = models.CharField(max_length=254, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=128)


class Song(models.Model):
    title = models.CharField(max_length=254)
    artist = models.ForeignKey(
        Artist, related_name='songs', null=True, blank=True)
    album = models.ForeignKey(
        Album, related_name='songs', null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    stream_count = models.IntegerField(null=True, blank=True)
    listener_count = models.IntegerField(null=True, blank=True)
    play_count = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
