from django import forms
from accounts.models import UserProfile
# from django.forms import ModelForm
# from django.core import serializers
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# import datetime

AcctCreation = False


class ExportForm(forms.Form):

    def save(self):
        return self.cleaned_data['export']


# Extends the normal user form to create a UserProfile object during sign-up
class SignupForm(forms.Form):
    AcctCreation = True

    def signup(self, request, user):
        # Appropriately populate the fields of the UserProfile object
        pass

