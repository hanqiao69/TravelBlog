from django.conf.urls import patterns, url
from views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'transcription.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^login/', login),
    # url(r'^logout/', logout),
    # url(r'^signup/',signup),
    # url(r'^legal/', legal),
    # url(r'^administration/',administration)),
    url(r'^home/$', home),
    url(r'^$', home),
    #url(r'^profile/(?P<user_id>[0-9]+)/$', profile),
    #url(r'^profile/public/(?P<username_user>[\w.@+-]+)/$', publicprofile),
    url(r'^profile/me/$', profileself),
    url(r'^profile/update/$', update, name='update'),
    url(r'^profile/update/image$', update_image, name='update_image'),
    url(r'^currency/$', currency),
    url(r'^climate/(?P<month>[\w.@+-]+)/$', climate),
    url(r'^countries/(?P<country_code>[\w.@+-]+)/$', country),
    url(r'^ranking/$', ranking),
    
)
urlpatterns += staticfiles_urlpatterns()
