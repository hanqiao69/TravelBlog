import datetime
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount
import hashlib
#---DATABASE-MODELS--------------------------------------------------------------------------------------------------------

class UserProfile(models.Model):
	user = models.OneToOneField(User) # Each UserProfile is uniquely associated with a User
	username = models.CharField(max_length=30)
	base_cal = models.TextField(null=True, blank=True)
	gen_first = models.BooleanField(default=False)
	def id(self):
		return user.id
	def profile_image_url(self):
#         """
#         Return the URL for the user's Facebook icon if the user is logged in via Facebook,
#         otherwise return the user's Gravatar URL
#         """
		fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
		google_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
		if len(fb_uid):
			return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
		elif len(google_uid):
			extra_data = google_uid[0].extra_data
			return extra_data["picture"]
		return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())
	def __unicode__(self):
		return self.username
class WeekCalendar(models.Model):
	start_date = models.DateField(null=True, blank=True)
	availability = models.TextField(null=True, blank=True)
	user = models.ManyToManyField(User, null=True, blank=True, related_name='owner')
	def user_names(self):
		return ', '.join([UserProfile.get(user=a).username for a in self.user.all()])
	def __unicode__(self):
		return self._id

class Group(models.Model):
	jointcal = models.TextField(null=True, blank=True)
	weeklycals = models.ManyToManyField(WeekCalendar, null=True, blank=True, related_name= 'groupcals')
	admin = models.ManyToManyField(User, null=True, blank=True, related_name='group_admin')
	members = models.ManyToManyField(User, null=True, blank=True, related_name='group_member')
	def admin_names(self):
		return ', '.join([a.username for a in self.admin.all()])
	admin_names.short_description = "Admins"
	def member_names(self):
		return ', '.join([a.username for a in self.members.all()])
	def weekly_cals(self):
		return ', '.join([WeekCalendar.objects.get(user=a.user).username for a in self.weeklycals.all()])
	member_names.short_description = "Members"
	def __unicode__(self):
		return str(self.id)


#---SIGNAL-HANDLERS--------------------------------------------------------------------------------------------------------

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


#---SIGNAL-LISTENERS--------------------------------------------------------------------------------------------------------


post_save.connect(create_user_profile, sender=User)

