# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

from .models import *


def index(request):
    context = {'active': 'home'}

    return render(request, 'journal/template.html', context)
