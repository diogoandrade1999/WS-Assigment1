from django.conf.urls import url
from django.urls import path
from shows.views import home, shows, directors, cast, actors


urlpatterns = [
    url(r'^$', home, name='home'),
    path('shows/', shows, name='shows'),
    path('directors/', directors, name='directors'),
    path('cast/', cast, name='cast'),
    path('actors/', actors, name='actors'),
    path('actors/<str:name>', actors, name='actors')
]
