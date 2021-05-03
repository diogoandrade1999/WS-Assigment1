from django.shortcuts import render, redirect
from shows.query import list_shows, list_directors, show_cast, list_actors


def home(request):
    return render(request, 'pages/home.html')


def shows(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        params = {'previous_page': page - 1, 'next_page': page + 1, 'shows': list_shows(page)}
        return render(request, 'pages/shows.html', params)
    return redirect(home)


def directors(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        params = {'previous_page': page - 1, 'next_page': page + 1, 'directors': list_directors(page)}
        return render(request, 'pages/directors.html', params)
    return redirect(home)


def cast(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        params = {'previous_page': page - 1, 'next_page': page + 1, 'cast': show_cast(page)}
        return render(request, 'pages/cast.html', params)
    return redirect(home)


def actors(request, name=None):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        if name:
            params = {'previous_page': page - 1, 'next_page': page + 1, 'actors': list_actors(page, name)}
        else:
            params = {'previous_page': page - 1, 'next_page': page + 1, 'actors': list_actors(page)}
        return render(request, 'pages/actors.html', params)
    return redirect(home)
