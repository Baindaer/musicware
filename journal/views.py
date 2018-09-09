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

    return render(request, 'journal/index.html', context)


def login(request):
    # Definiendo la funcion iniciar sesion con un requerimiento POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Usamos el metodo de autenticar de django para validar la informacion
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Contraseña correcta, se marca el usuario como activo
            auth.login(request, user)
            messages.success(request, 'Login sucessfully')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Autentication error, please check your credentials')
            return HttpResponseRedirect(reverse('login'))
    else:
        # Si no es un request tipo POST se renderiza el login
        return render(request, 'journal/login.html')


def composers(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'save':
            c_id = request.POST['composer_id'] or 0
            try:
                composer_id = Composer.objects.get(id=c_id)
            except models.ObjectDoesNotExist:
                composer_id = False
            if composer_id:
                composer_id.name = request.POST['composer_name']
                composer_id.period = request.POST['composer_period']
                composer_id.save()
                messages.success(request, 'Composer updated successfully')
            else:
                new_composer = Composer(
                    name=request.POST['composer_name'],
                    period=request.POST['composer_period'],
                    user=request.user
                )
                new_composer.save()
                messages.success(request, 'Composer saved successfully')
            return HttpResponseRedirect(reverse('composers'))
        if request.POST['submit'] == 'delete':
            c_id = request.POST['composer_id']
            try:
                composer_id = Composer.objects.get(id=c_id)
            except models.ObjectDoesNotExist:
                messages.warning(request, 'Composer not found')
                return HttpResponseRedirect(reverse('composers'))
            composer_id.delete()
            messages.success(request, 'Composer deleted successfully')
    composer_data = Composer.objects.filter(user_id=request.user).order_by('name')
    context = {
        'active': 'composers',
        'composers': composer_data,
    }

    return render(request, 'journal/composers.html', context)


def practice_items(request):
    composer_data = Composer.objects.filter(user_id=request.user).order_by('name')
    practice_item_data = PracticeItem.objects.filter(user_id=request.user).order_by('-date')
    if request.method == 'POST':
        if request.POST['submit'] == 'save':
            p_id = request.POST['item_id'] or 0
            try:
                item_id = PracticeItem.objects.get(id=p_id)
            except models.ObjectDoesNotExist:
                item_id = False
            if item_id:
                item_id.name = request.POST['item_name']
                item_id.composer_id = int(request.POST['item_composer'])
                item_id.self_appraisal = request.POST['item_self_appraisal']
                item_id.difficulty = request.POST['item_difficulty']
                item_id.type = request.POST['item_type']
                item_id.date = datetime.strptime(request.POST['item_date'], "%Y-%m-%d")
                item_id.save()
                messages.success(request, 'Item updated successfully')
            else:
                if request.POST['item_composer']:
                    composer = Composer.objects.get(id=request.POST['item_composer'])
                else:
                    composer = None
                new_item = PracticeItem(
                    name=request.POST['item_name'],
                    composer=composer,
                    self_appraisal=request.POST['item_self_appraisal'],
                    difficulty=request.POST['item_difficulty'],
                    type=request.POST['item_type'],
                    date=datetime.strptime(request.POST['item_date'], "%Y-%m-%d"),
                    user=request.user,
                )
                new_item.save()
                messages.success(request, 'Item saved successfully')
            return HttpResponseRedirect(reverse('practice_items'))
        if request.POST['submit'] == 'delete':
            p_id = request.POST['item_id']
            try:
                item_id = PracticeItem.objects.get(id=p_id)
            except models.ObjectDoesNotExist:
                messages.warning(request, 'Item not found')
                return HttpResponseRedirect(reverse('practice_items'))
            item_id.delete()
            messages.success(request, 'Item deleted successfully')
        if request.POST['submit'] == 'repertory_filter':
            practice_item_data = PracticeItem.objects.filter(user_id=request.user, type='Repertory').order_by('-date')
        if request.POST['submit'] == 'method_filter':
            practice_item_data = PracticeItem.objects.filter(user_id=request.user, type='Method').order_by('-date')
        if request.POST['submit'] == 'technique_filter':
            practice_item_data = PracticeItem.objects.filter(user_id=request.user, type='Technique').order_by('-date')
    context = {
        'active': 'practice_items',
        'practice_item_data': practice_item_data,
        'composers': composer_data,
    }
    return render(request, 'journal/practice_items.html', context)



