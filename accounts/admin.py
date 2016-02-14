from django.contrib import admin
from accounts.models import NormalUserProfile, CorporateProfile, Group, Entry, Post, Trip

class NormalUserProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'username', 'id', 'followers']


class CorporateProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'company', 'address', 'number']


class GroupAdmin(admin.ModelAdmin):
        list_display = ['admin_names', 'member_names']
class EntryAdmin(admin.ModelAdmin):
        list_display = ['user', 'latitude', 'longitude','geoname', 'text']
class PostAdmin(admin.ModelAdmin):
        list_display = ['user']
class TripAdmin(admin.ModelAdmin):
        list_display = ['user', 'name']

admin.site.register(NormalUserProfile, NormalUserProfileAdmin)
admin.site.register(CorporateProfile, CorporateProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Trip, TripAdmin)
