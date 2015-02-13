import os

from django import forms
from django.shortcuts import redirect, render_to_response
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponseRedirect
# from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
# from django.template import Context, Template
# from django.core import serializers
from accounts.models import CustomUser, Group
# import datetime
from django.contrib.auth.decorators import login_required
# from allauth.socialaccount.models import SocialToken
# from allauth.socialaccount.models import SocialAccount


# Create your views here.
def home(request):
    query = CustomUser.objects.all().filter(username=request.user)
    if len(query):
        return redirect('/profile/update')
    else:
        return render_to_response("index.html", RequestContext(request))


@login_required(login_url='/login')
def group(request, group_id):
    # user = CustomUser.objects.get(username=request.user)
    query = Group.objects.all().filter(id=group_id)
    group = query[0]
    users = group.members.all()
    members = []
    for user in users:
        user_profile = user.get_user_profile()
        members.append({"username": user.username,
                        "profile_image": user_profile.profile_image_url()})
    data = {'group': group, 'members': members}
    return render_to_response("group.html", data, RequestContext(request))


def brand(request):
    return render_to_response("brand.html", RequestContext(request))


@login_required(login_url='/login')
def groups(request):
    user = CustomUser.objects.get(username=request.user)
    user_profile = user.get_user_profile()
    groups = Group.objects.all().filter(admin=request.user)
    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile, 'groups': groups, 'username': user}
    return render_to_response("groups.html", data, RequestContext(request))


@login_required(login_url='/login')
def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user_profile = user.get_user_profile()

    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile}

    return render_to_response('profile.html', data, RequestContext(request))


def publicprofile(request, username_user):
    user = CustomUser.objects.get(username=username_user)
    user_profile = user.get_user_profile()

    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile, 'username': user}

    return render_to_response('profile.html', data, RequestContext(request))


@login_required(login_url='/login')
def profileself(request):
    print request
    user = CustomUser.objects.get(username=request.user)
    print user
    user_profile = user.get_user_profile()

    data = {'profile_image': user_profile.profile_image_url(),
            'profile': user_profile}

    return render_to_response('profile.html', data, RequestContext(request))


class UploadFileForm(forms.Form):
    image_file = forms.FileField(label='Select a file')


@login_required(login_url='/login')
def calupdate(request):
    if request.POST.get('mybtn'):
        string1 = ""
        for i in range(1, 337):
            print request.POST.get(str(i))
            if request.POST.get(str(i)) == 'true':
                string1 += "1"
            else:
                string1 += "0"
        user = CustomUser.objects.get(username=request.user)
        user_profile = user.get_user_profile()
        user_profile.save()
    if request.POST.get('gen_group'):
        new_group = Group.objects.create()
        new_group.admin.add(request.user)
        new_group.members.add(request.user)
        new_group.save()
        return redirect('/group/' + str(new_group.id))
    user = CustomUser.objects.get(username=request.user)
    print user
    user_profile = user.get_user_profile()
    print "hello"
    form = UploadFileForm()
    data = {'profile_image': user_profile.profile_image_url(),
            'profile': user_profile,
            'form': form}

    return render_to_response('calupdate.html', data, RequestContext(request))


def handle_uplaoded_file(user, file_):
    user_name = str(user)
    images_dir = 'static/user_images/'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    image_name = 'user_images/' + user_name
    user_profile = CustomUser.objects.get(username=user).get_user_profile()
    user_profile.profile_image = image_name
    user_profile.save()
    image_path = 'static/' + image_name
    print 'let\'s write to', image_path
    with open(image_path, 'wb+') as destination:
        for chunk in file_.chunks():
            destination.write(chunk)


@login_required(login_url='/login')
def update_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uplaoded_file(request.user, request.FILES['image_file'])
    return calupdate(request)


def compile_results(string1):
    print string1
