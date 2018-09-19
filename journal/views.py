# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Q

from .models import *


def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))

    # Total time
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(time) from journal_session WHERE user_id = {user}".format(user=request.user.id))
        total_time = cursor.fetchall()
    if total_time:
        total_time = total_time[0][0]
    else:
        total_time = 0

    # Week time
    with connection.cursor() as cursor:
        day_m7 = datetime.strftime(datetime.now() - timedelta(days=7), "%Y-%m-%d")
        cursor.execute("SELECT sum(time) from journal_session "
                       "WHERE user_id = {user} and date >= {date}".format(user=request.user.id, date=day_m7))
        week_time = cursor.fetchall()
    if week_time:
        week_time = week_time[0][0]
    else:
        week_time = 0


    context = {
        'active': 'home',
        'total_time': total_time,
        'week_time': week_time,
    }


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


def playlists(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'save':

            new_playlist = Playlist(
                name=request.POST['name'],
                user=request.user,
            )
            new_playlist.save()
    playlist_data = Playlist.objects.filter(user_id=request.user).order_by('id')
    context = {
        'active': 'playlists',
        'playlists': playlist_data,
    }
    return render(request, 'journal/playlists.html', context)


def playlist_view(request, playlist_id):
    try:
        playlist_data = Playlist.objects.get(id=playlist_id)
    except models.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('playlists'))
    playlist_lines = PlaylistLine.objects.filter(playlist=playlist_id).order_by('sequence')
    item_data = PracticeItem.objects.filter(user_id=request.user).order_by('name')
    context = {
        'active': 'playlists',
        'playlist': playlist_data,
        'playlist_lines': playlist_lines,
        'available_items': item_data
    }
    if request.method == 'POST':
        if request.POST['submit'] == 'save':
            item = PracticeItem.objects.get(id=request.POST['item'])
            new_line = PlaylistLine(
                item=item,
                playlist=playlist_data,
                sequence=100,
            )
            new_line.save()
        if request.POST['submit'] == 'rename':
            playlist_data.name = request.POST['name']
            playlist_data.save()
            messages.success(request, 'Playlist renamed successfully')
        if request.POST['submit'] == 'delete_playlist':
            playlist_data.delete()
            messages.success(request, 'Playlist removed successfully')
            return HttpResponseRedirect(reverse('playlists'))
        if request.POST['submit'] == 'done':
            line_id = PlaylistLine.objects.get(id=request.POST['id'])
            time = datetime.strptime(request.POST['timer'], "%H:%M:%S").minute
            if time:
                new_session = Session(
                    user=request.user,
                    practice_item=line_id.item,
                    time=time,
                    rate=int(request.POST['selected_rating']),
                    note=request.POST['notes'],
                    date=datetime.now(),
                )
                new_session.save()
                messages.success(request, "Session saved")
            else:
                messages.error(request, "Not enought practice time to register")

    return render(request, 'journal/playlist_view.html', context)


def delete_playlist_line(request, line_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    playlist_line = PlaylistLine.objects.get(id=line_id)
    playlist = playlist_line.playlist.id
    playlist_line.delete()
    return HttpResponseRedirect(reverse('playlist_view', args=(playlist,)))


def move_playlist_line(request, line_id, dir):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    playlist_line = PlaylistLine.objects.get(id=line_id)
    playlist = playlist_line.playlist.id
    playlist_lines = PlaylistLine.objects.filter(playlist=playlist).order_by('sequence')
    seq, from_seq, to_seq = 1, 0, 0
    for line in playlist_lines:
        line.sequence = seq
        if line.id == line_id:
            from_seq = seq
        seq += 1
        line.save()
    if dir == 'down':
        to_seq = from_seq + 1
    elif dir == 'up':
        to_seq = from_seq - 1
    for line in playlist_lines:
        if line.sequence == to_seq:
            line.sequence = from_seq
            line.save()
    playlist_line.sequence = to_seq
    playlist_line.save()

    return HttpResponseRedirect(reverse('playlist_view', args=(playlist,)))


def sessions(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('login'))
    sd_list = []
    date_data = []
    by_day = False
    if request.method == 'POST':
        if request.POST['submit'] == 'by_week':
            with connection.cursor() as cursor:
                cursor.execute("SELECT strftime('%Y-%W', js.date), jp.name, jc.name, jp.type, "
                               "sum(js.time), round(avg(js.rate),0), group_concat(js.note, '|') "
                               "FROM journal_session js "
                               "INNER JOIN journal_practiceitem jp ON js.practice_item_id = jp.id "
                               "LEFT JOIN journal_composer jc on jp.composer_id = jc.id "
                               "WHERE js.user_id = {user} GROUP BY js.practice_item_id, strftime('%Y-%W', js.date) "
                               "ORDER BY js.date DESC".format(user=request.user.id))
                session_data = cursor.fetchall()
                cursor.execute("SELECT strftime('%Y-%W', js.date), sum(js.time) "
                               "FROM journal_session js "
                               "WHERE js.user_id = {user} GROUP BY strftime('%Y-%W', js.date) "
                               "ORDER BY js.date DESC".format(user=request.user.id))
                date_data = cursor.fetchall()
            sd_list = []
            for item in session_data:
                item2 = list(item)
                notes = item[6].split("|")
                a = ['']
                if notes != a:
                    item2[6] = notes
                else:
                    item2[6] = False
                sd_list.append(item2)
        if request.POST['submit'] == 'by_day':
            by_day = True
    else:
        by_day = True

    if by_day:
        with connection.cursor() as cursor:
            cursor.execute("SELECT js.date, jp.name, jc.name, jp.type, "
                           "sum(js.time), round(avg(js.rate),0), group_concat(js.note, '|') "
                           "FROM journal_session js "
                           "INNER JOIN journal_practiceitem jp ON js.practice_item_id = jp.id "
                           "LEFT JOIN journal_composer jc on jp.composer_id = jc.id "
                           "WHERE js.user_id = {user} GROUP BY js.practice_item_id, js.date "
                           "ORDER BY js.date DESC".format(user=request.user.id))
            session_data = cursor.fetchall()
            cursor.execute("SELECT js.date, sum(js.time) "
                           "FROM journal_session js "
                           "WHERE js.user_id = {user} GROUP BY js.date "
                           "ORDER BY js.date DESC".format(user=request.user.id))
            date_data = cursor.fetchall()
        sd_list = []
        for item in session_data:
            item2 = list(item)
            notes = item[6].split("|")
            a = ['']
            if notes != a:
                item2[6] = notes
            else:
                item2[6] = False
            sd_list.append(item2)

    context = {
        'active': 'sessions',
        'sessions': sd_list,
        'date_list': date_data
    }
    return render(request, 'journal/sessions.html', context)




