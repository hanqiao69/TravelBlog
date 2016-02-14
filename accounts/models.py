# import datetime
# from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django import forms
# from django.contrib.auth.models import User
# from allauth.account.signals import user_logged_in
# from django.contrib.auth.signals import user_logged_out
# from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount
# import hashlib
import cPickle


# ---DATABASE-MODELS------------------------------------------------------
class CustomUser(AbstractUser):
    corporate = models.BooleanField(default=False)

    def get_user_profile(self):
        print(self)
        print(self.corporate)
        if(self.corporate is False):
            return NormalUserProfile.objects.get(user=self)
        else:
            return CorporateProfile.objects.get(user=self)

    REQUIRED_FIELDS = ["email"]


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)

    class Meta:
        abstract = True


class NormalUserProfile(UserProfile):
    username = models.CharField(max_length=500)
    profile_image = models.TextField(null=True, blank=True)
    provider = models.TextField(verbose_name='provider',null=True, blank=True)
    fullname = models.TextField(null=True, blank=True)
    counts = models.TextField(null=True, blank=True)
    posts = models.IntegerField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    numfollow = models.IntegerField(null=True, blank=True)
    instagramid = models.TextField(null=True, blank=True)
    search_cache = models.TextField(null=True, blank=True)

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

class Group(models.Model):
    jointcal = models.TextField(null=True, blank=True)
    admin = models.ManyToManyField(CustomUser, null=True, blank=True,
                                   related_name='group_admin')
    members = models.ManyToManyField(CustomUser, null=True, blank=True,
                                     related_name='group_member')

    def admin_names(self):
        return ', '.join([a.username for a in self.admin.all()])
    admin_names.short_description = "Admins"

    def member_names(self):
        return ', '.join([a.username for a in self.members.all()])

    member_names.short_description = "Members"

    def __unicode__(self):
        return str(self.id)
class Photo(models.Model):
    name = models.TextField(null=True, blank=True)
    link = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
class Entry(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geoname = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    photos = models.ManyToManyField(Photo, null=True, blank=True)
class Post(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    entries = models.ManyToManyField(Entry, null=True, blank=True)
class Trip(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser)
    posts = models.ManyToManyField(Post, null=True, blank=True)
# ---SIGNAL-HANDLERS-----------------------------------------------------------

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.corporate is False:
            NormalUserProfile.objects.create(user=instance)

        else:
            CorporateProfile.objects.create(user=instance)


def prepopulate_profile(sender, instance, created, **kwargs):
    if created:
        social_account = instance
        instance = instance.user
        user_profile = NormalUserProfile.objects.get(user=instance)
        uextra = social_account.extra_data
        extra = dict([(str(k), v) for k, v in uextra.items()])
        user_profile.username = extra.get('username')
        user_profile.profile_image = extra.get('profile_picture')
        user_profile.fullname = extra.get('fullname')
        user_profile.instagramid = extra.get('id')
        user_profile.provider = social_account.provider
        user_profile.save()
post_save.connect(prepopulate_profile, sender=SocialAccount)

# ---SIGNAL-LISTENERS--------------------------------------------------------------------------------------------------------


post_save.connect(create_user_profile, sender=CustomUser)


