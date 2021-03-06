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
    url(r'^trip/(?P<tripid>[\w.@+-]+)/upload/$', upload, name='trip_upload'),
    url(r'^trip/(?P<tripid>[\w.@+-]+)/$', trip, name='trip'),
    url(r'^profile/update/image$', update_image, name='update_image'),
    url(r'^ajax_calls/search/', autocompleteModel),
    url(r'^search/$', search, name='search'),
    
)
urlpatterns += staticfiles_urlpatterns()
