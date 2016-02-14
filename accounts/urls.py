from django.conf.urls import patterns, url
from views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^home/$', home),
    url(r'^$', home),
    url(r'^profile/me/$', profileself),
    url(r'^profile/update/$', update, name='update'),
    url(r'^profile/trips/$', trips, name='trips'),
    url(r'^trip/$', trip, name='trip'),
    url(r'^profile/update/image$', update_image, name='update_image'),
    url(r'^ajax_calls/search/', autocompleteModel),
    url(r'^search/$', search, name='search'),
    
)
urlpatterns += staticfiles_urlpatterns()
