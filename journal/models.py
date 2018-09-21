# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Composer(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    name = models.CharField('Name', max_length=64)
    period = models.CharField('Music era', max_length=64)

    def __str__(self):
        return self.name


class PracticeItem(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    name = models.CharField('Name', max_length=64)
    composer = models.ForeignKey('Composer', on_delete="models.PROTECT", null=True, blank=True)
    date = models.DateField('Date added')
    type = models.CharField('Type', max_length=32)
    self_appraisal = models.IntegerField('Self Appraisal')
    difficulty = models.IntegerField('Difficulty')

    def __str__(self):
        return self.name


class Playlist(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField('Name', max_length=64)
    user = models.ForeignKey(User, on_delete="models.CASCADE")

    def __str__(self):
        return self.name

    def get_lines(self):
        return PlaylistLine.objects.filter(playlist=self.id).count()


class PlaylistLine(models.Model):
    id = models.IntegerField(primary_key=True)
    sequence = models.IntegerField('Sequence')
    item = models.ForeignKey(PracticeItem, on_delete="models.CASCADE")
    playlist = models.ForeignKey(Playlist, on_delete="models.CASCADE")

    def __str__(self):
        return self.item.name


class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    practice_item = models.ForeignKey(PracticeItem, on_delete="models.PROTECT")
    time = models.IntegerField('Practiced time')
    rate = models.FloatField('Rate')
    note = models.TextField('Notes', max_length=256, blank=True, null=True)
    date = models.DateField('Date')
    comment = models.TextField('Comment', max_length=256, blank=True, null=True)

    def __str__(self):
        return str(self.date) + ' ' + str(self.practice_item.name)




