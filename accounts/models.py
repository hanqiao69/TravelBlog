# import datetime
# from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from allauth.account.signals import user_logged_in
# from django.contrib.auth.signals import user_logged_out
# from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount
# import hashlib
import cPickle

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=500)
    current = models.FloatField(null=True, blank=True, max_digits=19, decimal_places=3)
    current_updated = models.DateField(null=True, blank=True)
    five_yr_mean = models.FloatField(null=True, blank=True, max_digits=19, decimal_places=3)
    five_yr_stdev = models.FloatField(null=True, blank=True, max_digits=19, decimal_places=3)
    #five_yr_values = models.TextField(null=True, blank=True)
    z_score = models.FloatField(null=True, blank=True, max_digits=5, decimal_places=3)
    #percent_change = models.FloatField(null=True, blank=True)

class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=500)
    currency = models.ManyToManyField(Currency, null=True, blank=True)
    temperature = models.TextField(null=True, blank=True) #temperature is array of length 13 (fahrenheit), one for each month and avg
    rainfall = models.TextField(null=True, blank=True) #precip is array of length 13 (mm), one for each month and avg
    rainy_dry = models.TextField(null=True, blank=True) #rainy_dry is array of length 12, one for each month
    #homocides = models.IntegerField(null=True, blank=True)
    #peace_index = models.TextField(null=True, blank=True)


# ---DATABASE-MODELS------------------------------------------------------
class CustomUser(AbstractUser):
    corporate = models.BooleanField(default=False)

    def get_user_profile(self):
        print(self)
        print(self.corporate)
        if(self.corporate is False):
            return InfluencerProfile.objects.get(user=self)
        else:
            return CorporateProfile.objects.get(user=self)

    REQUIRED_FIELDS = ["email"]


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)

    class Meta:
        abstract = True


class InfluencerProfile(UserProfile):
    username = models.CharField(max_length=500)
    profile_image = models.TextField(null=True, blank=True)
    provider = models.TextField(verbose_name='provider',null=True, blank=True)
    fullname = models.TextField(null=True, blank=True)
    counts = models.TextField(null=True, blank=True)
    posts = models.IntegerField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    numfollow = models.IntegerField(null=True, blank=True)
    instagramid = models.TextField(null=True, blank=True)

    def profile_image_url(self):
        return self.profile_image

    def id(self):
        return self.user.id
#     def profile_image_url(self):
#           """
#           Return the URL for the user's Facebook icon if the user is logged
#           in via Facebook, otherwise return the user's Gravatar URL
#           """
#         fb_uid = SocialAccount.objects.filter(user_id=self.user.id,
#                                               provider='facebook')
#         google_uid = SocialAccount.objects.filter(user_id=self.user.id,
#                                                   provider='google')
#         if len(fb_uid):
#             return ("http://graph.facebook.com/{}/picture?width=40&height=40"
#                     .format(fb_uid[0].uid))
#         elif len(google_uid):
#             extra_data = google_uid[0].extra_data
#             return extra_data["picture"]
#         return ("http://www.gravatar.com/avatar/{}?s=40"
#                 .format(hashlib.md5(self.user.email).hexdigest()))

    def __unicode__(self):
        return self.username

class CorporateProfile(UserProfile):
    company = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=2000)

    def __unicode__(self):
        return self.company



class WeekCalendar(models.Model):
    start_date = models.DateField(null=True, blank=True)
    availability = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(CustomUser, null=True, blank=True,
                                  related_name='owner')

    def user_names(self):
        return ', '.join(
            [UserProfile.get(user=a).username for a in self.user.all()])

    def __unicode__(self):
        return self._id


class Group(models.Model):
    jointcal = models.TextField(null=True, blank=True)
    weeklycals = models.ManyToManyField(WeekCalendar, null=True, blank=True,
                                        related_name='groupcals')
    admin = models.ManyToManyField(CustomUser, null=True, blank=True,
                                   related_name='group_admin')
    members = models.ManyToManyField(CustomUser, null=True, blank=True,
                                     related_name='group_member')

    def admin_names(self):
        return ', '.join([a.username for a in self.admin.all()])
    admin_names.short_description = "Admins"

    def member_names(self):
        return ', '.join([a.username for a in self.members.all()])

    def weekly_cals(self):
        return ', '.join(
            [WeekCalendar.objects.get(user=a.user).username
             for a in self.weeklycals.all()])
    member_names.short_description = "Members"

    def __unicode__(self):
        return str(self.id)


# ---SIGNAL-HANDLERS-----------------------------------------------------------

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.corporate is False:
            InfluencerProfile.objects.create(user=instance)

        else:
            CorporateProfile.objects.create(user=instance)


def prepopulate_profile(sender, instance, created, **kwargs):
    if created:
        social_account = instance
        instance = instance.user
        user_profile = InfluencerProfile.objects.get(user=instance)
        uextra = social_account.extra_data
        extra = dict([(str(k), v) for k, v in uextra.items()])
        user_profile.username = extra.get('username')
        user_profile.profile_image = extra.get('profile_picture')
        user_profile.fullname = extra.get('fullname')
        user_profile.counts = extra.get('counts')
        ucounts = dict([(str(k), v) for k, v in extra.get('counts').items()])
        user_profile.posts = ucounts.get('media')
        user_profile.followers = ucounts.get('followed_by')
        user_profile.numfollow = ucounts.get('follows')
        user_profile.instagramid = extra.get('id')
        user_profile.provider = social_account.provider
        user_profile.save()
post_save.connect(prepopulate_profile, sender=SocialAccount)

# ---SIGNAL-LISTENERS--------------------------------------------------------------------------------------------------------


post_save.connect(create_user_profile, sender=CustomUser)
