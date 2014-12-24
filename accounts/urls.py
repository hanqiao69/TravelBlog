from django.conf.urls import patterns, include, url
from views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'transcription.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#url(r'^login/', login),
	# url(r'^logout/', logout),
	# url(r'^signup/',signup),
	# url(r'^legal/', legal),
	# url(r'^administration/',administration)),
	url(r'^home/$', home),
	url(r'^$', home),
	url(r'^profile/(?P<user_id>[0-9]+)/$', profile),
	url(r'^profile/public/(?P<username_user>[\w.@+-]+)/$', publicprofile),
	url(r'^profile/me/$', profileself),
	url(r'^profile/me/groups$', groups),
	url(r'^group/(?P<group_id>[0-9]+)/$', group),
	url(r'^profile/update/$', calupdate),
)
