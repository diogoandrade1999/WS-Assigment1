from django.shortcuts import render, redirect
from shows.query import *
import math


def home(request):
    return render(request, 'pages/home.html')


def shows(request):
    if request.method == 'GET' or request.method == 'POST':
        params = {'types': list_shows_type(),
                  'countries': sorted(list_shows_countries()),
                  'listed_in': sorted(list_shows_listed_in()),
                  }
        if request.method == 'GET':
            page = request.GET.get('page')
            if page == None:
                page = 0
                params['t_checked'] = params['types']
                params['c_checked'] = params['countries']
                params['l_checked'] = params['listed_in']
                params['shows'] = list_shows(page)
            else:
                page = int(page)
                params['title'] = request.GET.get('searchShowTitle')
                params['t_checked'] = request.GET.getlist('searchShowType')
                params['c_checked'] = request.GET.getlist('searchShowCountry')
                params['l_checked'] = request.GET.getlist('searchShowListedIn')
                params['shows'] = search_shows(page, params['title'], params['t_checked'], params['c_checked'], params['l_checked'])  
        elif request.method == 'POST':
            page = request.POST.get('page')
            if page == None:
                page = 0
            page = int(page)
            params['title'] = request.POST.get('searchShowTitle')
            params['t_checked'] = request.POST.getlist('searchShowType')
            params['c_checked'] = request.POST.getlist('searchShowCountry')
            params['l_checked'] = request.POST.getlist('searchShowListedIn')
            params['shows'] = search_shows(page, params['title'], params['t_checked'], params['c_checked'], params['l_checked'])

        params['previous_page'] = page - 1 if page > 0 else None
        params['next_page'] = page + 1 if len(params['shows']) == 30 else None
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


def actors(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if page == None:
            page = 0
        page = int(page)
        params = {'previous_page': page - 1, 'next_page': page + 1, 'actors': list_actors(page)}
        return render(request, 'pages/actors.html', params)
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
