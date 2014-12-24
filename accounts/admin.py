from django.contrib import admin
from accounts.models import UserProfile, Group, WeekCalendar
class UserProfileAdmin(admin.ModelAdmin): 
		list_display  = ['user','username', 'id', 'base_cal', 'gen_first']

class GroupAdmin(admin.ModelAdmin):
		list_display = ['jointcal','admin_names','member_names', 'weekly_cals']
class WeekCalendarAdmin(admin.ModelAdmin):
		list_display = ['start_date','user_names','availability']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(WeekCalendar, WeekCalendarAdmin)
