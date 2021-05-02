from django.shortcuts import render, redirect
from shows.query import list_shows, list_directors


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
