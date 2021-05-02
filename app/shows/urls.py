from django.urls import path
from django.conf.urls import url
from shows.views import home, shows, directors


urlpatterns = [
    url(r'^$', home, name='home'),
    path('shows/', shows, name='shows'),
    path('directors/', directors, name='directors'),
]
