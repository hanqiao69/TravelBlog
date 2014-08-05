import datetime
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.account.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out

#---DATABASE-MODELS--------------------------------------------------------------------------------------------------------

class UserProfile(models.Model):
	user = models.OneToOneField(User) # Each UserProfile is uniquely associated with a User
	username = models.CharField(max_length=30)
	calendarapp = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return self.username


class Group(models.Model):
	jointcal = models.TextField(null=True, blank=True)
	admin = models.ManyToManyField(User, null=True, blank=True, related_name='group_admin')
	members = models.ManyToManyField(User, null=True, blank=True, related_name='group_member')
	def admin_names(self):
		return ', '.join([UserProfile.get(user=a).username for a in self.admin.all()])
	admin_names.short_description = "Admins"
	def member_names(self):
		return ', '.join([UserProfile.get(user=a).username for a in self.members.all()])
	member_names.short_description = "Members"
	def __unicode__(self):
		return self._id


#---SIGNAL-HANDLERS--------------------------------------------------------------------------------------------------------

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


#---SIGNAL-LISTENERS--------------------------------------------------------------------------------------------------------


post_save.connect(create_user_profile, sender=User)

