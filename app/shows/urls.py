from django.urls import path
from django.conf.urls import url
from shows.views import home, shows, show, directors, person


urlpatterns = [
    url(r'^$', home, name='home'),
    path('shows/', shows, name='shows'),
    path('show/', show, name='show'),
    path('directors/', directors, name='directors'),
    path('person/', person, name='person'),
]
