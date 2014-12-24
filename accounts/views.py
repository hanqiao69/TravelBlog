from django.shortcuts import *
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.template import Context, Template
from django.core import serializers
from accounts.models import UserProfile, User, Group
import datetime
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount

# Create your views here.
def home(request):
    query = User.objects.all().filter(username=request.user)
    if len(query):
        return redirect('/profile/update')
    else:
	   return render_to_response("index.html", RequestContext(request))
@login_required(login_url='/login')
def group(request,group_id):
    userr = User.objects.get(username=request.user)
    query = Group.objects.all().filter(id=group_id)
    group = query[0]
    users = group.members.all()
    members = []
    for user in users:
        queryusers = UserProfile.objects.all().filter(user=user)
        profi=queryusers[0]
        members.append({"username": user.username, "profile_image":profi.profile_image_url()})
    data = {'group':group, 'members':members}
    return render_to_response("group.html", data, RequestContext(request))
def groups(request):
    userr = User.objects.get(username=request.user)
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]
    groups = Group.objects.all().filter(admin=request.user)
    data = {'profile_image': user_profile.profile_image_url(), 'prof': user_profile, 'groups':groups, 'username':userr}
    return render_to_response("groups.html", data, RequestContext(request))
@login_required(login_url='/login')
def profile(request,user_id):
    userr = User.objects.get(id =user_id)
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]

    data = {'profile_image': user_profile.profile_image_url(), 'prof': user_profile}
                
    return render_to_response('profile.html', data, RequestContext(request))
def publicprofile(request,username_user):
    userr = User.objects.get(username =username_user)
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]

    data = {'profile_image': user_profile.profile_image_url(), 'prof': user_profile, 'username':userr, 'base_cal': user_profile.base_cal}
                
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
        for i in range(1,337):
            print request.POST.get(str(i))
            if request.POST.get(str(i)) =='true':
                string1 += "1"
            else:
                string1 +="0"
        userr = User.objects.get(username=request.user)
        query = UserProfile.objects.all().filter(user=userr)
        user_profile = query[0]
        user_profile.base_cal = string1
        user_profile.save()
    if(request.POST.get('gen_group')):
        newGroup = Group.objects.create()
        newGroup.admin.add(request.user)
        newGroup.members.add(request.user)
        newGroup.save()
        return redirect('/group/'+str(newGroup.id))
    print(request)
    userr = User.objects.get(username=request.user)
    print userr
    query = UserProfile.objects.all().filter(user=userr)
    user_profile = query[0]
    print "hello"
    print user_profile.base_cal
    data = {'profile_image': user_profile.profile_image_url(), 'profile': user_profile, 'base_cal': user_profile.base_cal}
                
    return render_to_response('calupdate.html', data, RequestContext(request))
def compileResults(string1):
	print string1