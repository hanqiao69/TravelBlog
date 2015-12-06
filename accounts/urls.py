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
    url(r'^profile/update/image$', update_image, name='update_image'),
    url(r'^currency/$', currency),
    url(r'^climate/(?P<month>[\w.@+-]+)/$', climate),
    url(r'^countries/(?P<country_code>[\w.@+-]+)/$', country),
    url(r'^ranking/$', ranking),
    url(r'^ajax_calls/search/', autocompleteModel),
    url(r'^search/$', search, name='search'),
    
)
urlpatterns += staticfiles_urlpatterns()
