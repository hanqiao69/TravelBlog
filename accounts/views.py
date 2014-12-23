from django.shortcuts import *
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.template import Context, Template
from django.core import serializers
from accounts.models import UserProfile, User
import datetime
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount

# Create your views here.
def home(request):
	return render_to_response("index.html", RequestContext(request))

@login_required(login_url='/login')
def profile(request,user_id):
    userr = User.objects.get(id =user_id)
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]

    data = {'profile_image': user_profile.profile_image_url(), 'prof': user_profile}
                
    return render_to_response('profile.html', data, RequestContext(request))

@login_required(login_url='/login')
def profileself(request):
    print(request)
    userr = User.objects.get(username=request.user)
    print userr
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]

    data = {'profile_image': user_profile.profile_image_url(), 'profile': user_profile}
                
    return render_to_response('profile.html', data, RequestContext(request))
@login_required(login_url='/login')
def calupdate(request):
    if(request.POST.get('mybtn')):
        string1 = ""
        for i in range(1,10):
            print request.POST.get(str(i))
            if request.POST.get(str(i)) =='true':
                string1 += "1"
            else:
                string1 +="0"
        compileResults(string1)
    print(request)
    userr = User.objects.get(username=request.user)
    print userr
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]

    data = {'profile_image': user_profile.profile_image_url(), 'profile': user_profile}
                
    return render_to_response('calupdate.html', data, RequestContext(request))
def compileResults(string1):
	print string1