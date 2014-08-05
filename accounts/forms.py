from django import forms
from accounts.models import UserProfile, User
from django.forms import ModelForm
from django.core import serializers
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

AcctCreation = False

class ExportForm(forms.Form):
	#Export Form shows two radio buttons for the type of data to export and then exports user requested data
	CHOICES = [('1','Export Samples'),
	('2','Export Users for Compensation')]
	export = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True)
	def save(self):
		return self.cleaned_data['export']

# extends the normal user form in order to create a UserProfile object during sign-up
class SignupForm(forms.Form): 
	AcctCreation = True
	def signup(self, request, user):
		# Appropriately populate the fields of the UserProfile object
		UserProfileProfile = UserProfile.objects.get(user = user)
		UserProfileProfile.username = user.username
		
		#telemetry event saves the number of optional fields that were included in signup; event is linked with user id; 
		#the message includes the fields that were filled out
		UserProfileProfile.save()

		#  HOW TO CHECK IF HAS BEEN POSTED TO /SIGNUP/ AND, ONCE THAT'S BEEN DONE, IF IT WAS SAVED??
		# @receiver(post_save)
		# def success(sender, **kwargs):
		# 	if AcctCreation: 
		# 		if not post_save.created:
		# 			telemetry = TelemetryEvent.objects.create(event_type=Reference.ecodes[8][0])
		# 			telemetry.atid = UserProfile.objects.get(user=user)
		# 			telemetry.save()
		# 			AcctCreation = False
