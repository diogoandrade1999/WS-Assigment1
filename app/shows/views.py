from django.shortcuts import render, redirect
from shows.query import list_shows, list_directors, person_detail, show_detail


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


def show(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        if title == None:
            return redirect(shows)
        params = {'title': title, 'show': show_detail(title)}
        return render(request, 'pages/show.html', params)
    return redirect(shows)


def directors(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        params = {'previous_page': page - 1, 'next_page': page + 1, 'directors': list_directors(page)}
        return render(request, 'pages/directors.html', params)
    return redirect(home)


def person(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if name == None:
            return redirect(home)
        directorof, castof = person_detail(name)
        params = {'name': name, 'directorof': directorof, 'castof': castof}
        return render(request, 'pages/person.html', params)
    return redirect(home)
