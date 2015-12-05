from django.contrib import admin
from accounts.models import NormalUserProfile, CorporateProfile, Group, \
    Country, Currency

class NormalUserProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'username', 'id', 'followers']


class CorporateProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'company', 'address', 'number']


class GroupAdmin(admin.ModelAdmin):
        list_display = ['admin_names', 'member_names']

class CountryAdmin(admin.ModelAdmin):
        list_display = ['name', 'code']

class CurrencyAdmin(admin.ModelAdmin):
        list_display = ['name', 'code', 'five_yr_mean', 'current']

admin.site.register(NormalUserProfile, NormalUserProfileAdmin)
admin.site.register(CorporateProfile, CorporateProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
