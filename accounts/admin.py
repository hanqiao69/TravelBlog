from django.contrib import admin
from accounts.models import InfluencerProfile, CorporateProfile, Group, WeekCalendar
class InfluencerProfileAdmin(admin.ModelAdmin): 
		list_display  = ['user','username', 'id', 'followers']
class CorporateProfileAdmin(admin.ModelAdmin): 
		list_display  = ['user','company', 'address', 'number']

class GroupAdmin(admin.ModelAdmin):
		list_display = ['jointcal','admin_names','member_names', 'weekly_cals']
class WeekCalendarAdmin(admin.ModelAdmin):
		list_display = ['start_date','user_names','availability']

admin.site.register(InfluencerProfile, InfluencerProfileAdmin)
admin.site.register(CorporateProfile, CorporateProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(WeekCalendar, WeekCalendarAdmin)
