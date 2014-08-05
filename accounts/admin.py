from django.contrib import admin
from models import UserProfile, Group
class UserProfileAdmin(admin.ModelAdmin): 
		list_display = ('username', 'calendarapp')

class GroupAdmin(admin.ModelAdmin):
		list_display = ('jointcal','admin_names','member_names')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
