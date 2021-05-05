from django.urls import path
from django.conf.urls import url
from shows.views import home, shows, show, directors, actors, person, add


urlpatterns = [
    url(r'^$', home, name='home'),
    path('shows/', shows, name='shows'),
    path('show/', show, name='show'),
    path('directors/', directors, name='directors'),
    path('actors/', actors, name='actors'),
    path('person/', person, name='person'),
    path('add/', add, name='add')
]
