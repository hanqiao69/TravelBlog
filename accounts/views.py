from django.shortcuts import *
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.template import Context, Template
from django.core import serializers
from accounts.models import UserProfile, User
import datetime

# Create your views here.
def home(request):
	return render_to_response("index.html", RequestContext(request))

