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
