from django.contrib import admin
from accounts.models import NormalUserProfile, CorporateProfile, Group, \
    Country

class NormalUserProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'username', 'id', 'followers']


class CorporateProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'company', 'address', 'number']


class GroupAdmin(admin.ModelAdmin):
        list_display = ['jointcal', 'admin_names', 'member_names']

class CountryAdmin(admin.ModelAdmin):
        list_display = ['name', 'code']


admin.site.register(NormalUserProfile, NormalUserProfileAdmin)
admin.site.register(CorporateProfile, CorporateProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Country, CountryAdmin)
