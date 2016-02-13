import os
import operator
import json
import ast
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.shortcuts import redirect, render_to_response
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponseRedirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.forms.models import model_to_dict
# from django.template import Context, Template
# from django.core import serializers
from accounts.models import CustomUser
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from allauth.socialaccount.models import SocialToken
# from allauth.socialaccount.models import SocialAccount
# Create your views here.
def home(request):
    #query = CustomUser.objects.all().filter(username=request.user)
    #if len(query):
    #    return redirect('/profile/update')
    #else:
  return render_to_response('base.html', RequestContext(request))
        #return render_to_response("index.html", RequestContext(request))
def autocompleteModel(request):
  if request.is_ajax():
    q = request.GET.get('term', '').capitalize()
    search_qs = Country.objects.filter(name__startswith=q)
    results = []
    print q
    for r in search_qs:
      results.append(r.name)
    print results
    data = json.dumps(results)
  else:
      data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)
def search(request):
    if request.method == "POST":
      country = request.POST.get("txtSearch").capitalize()
      try:
        country_found = Country.objects.get(name=country)
        return redirect('/countries/'+country_found.code)
      except ObjectDoesNotExist:
        pass
    countries = Country.objects.all().order_by('name')
    data = {"countries": countries}
    return render_to_response('filter_countries.html', data, RequestContext(request))

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user_profile = user.get_user_profile()

    data = {'profile_image': user_profile.profile_image_url(),
            'profile': user_profile}

    return render_to_response('profile.html', data, RequestContext(request))

def publicprofile(request, username_user):
    user = CustomUser.objects.get(username=username_user)
    user_profile = user.get_user_profile()

    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile, 'username': user}

    return render_to_response('profile.html', data, RequestContext(request))


@login_required(login_url='/accounts/login')
def profileself(request):
    print request
    user = CustomUser.objects.get(username=request.user)
    print user
    user_profile = user.get_user_profile()

    search_cache = None
    print user_profile.search_cache
    if user_profile.search_cache:
      search_cache = json.loads(user_profile.search_cache)
    print search_cache
    if request.method == 'POST':
      request.session['search_query'] = request.POST.get("query_data")
      return redirect('/ranking')
    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile, 'search_cache': search_cache}

    return render_to_response('profile.html', data, RequestContext(request))

class UploadFileForm(forms.Form):
    image_file = forms.FileField(label='Upload a new profile image')


@login_required(login_url='/accounts/login')
def update(request):
    user = CustomUser.objects.get(username=request.user)
    print user
    user_profile = user.get_user_profile()
    profile_image = user_profile.profile_image_url()
    print "hello"
    form = UploadFileForm()
    data = {'profile_image': profile_image,
            'profile': user_profile,
            'form': form}

    return render_to_response('update.html', data, RequestContext(request))


def handle_uploaded_file(user, file_):
    user_name = str(user)
    images_dir = 'brandplug/static/user_images/'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    image_name = 'user_images/' + user_name
    user_profile = CustomUser.objects.get(username=user).get_user_profile()
    user_profile.profile_image = image_name
    user_profile.save()
    image_path = 'brandplug/static/' + image_name
    print 'let\'s write to', image_path
    with open(image_path, 'wb+') as destination:
        for chunk in file_.chunks():
            destination.write(chunk)


@login_required(login_url='/accounts/login')
def update_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.user, request.FILES['image_file'])
    return update(request)

