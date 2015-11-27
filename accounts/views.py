import os
import operator

from django import forms
from django.shortcuts import redirect, render_to_response
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponseRedirect
# from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.forms.models import model_to_dict
# from django.template import Context, Template
# from django.core import serializers
from accounts.models import CustomUser, Group, Country
# import datetime
from django.contrib.auth.decorators import login_required
# from allauth.socialaccount.models import SocialToken
# from allauth.socialaccount.models import SocialAccount
precip_url = {"jan": "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=1883644005&amp;format=interactive",
       "feb": "",
       "mar": "",
       "apr": "",
       "may": "",
       "jun": "",
       "jul": "",
       "aug": "",
       "sep": "",
       "oct": "",
       "nov": "",
       "dec": "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=1883644005&amp;format=interactive"}
precip_chart_url = {"jan": "",
       "feb": "",
       "mar": "",
       "apr": "",
       "may": "",
       "jun": "",
       "jul": "",
       "aug": "",
       "sep": "",
       "oct": "",
       "nov": "",
       "dec": "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=2014329076&amp;format=interactive"}
temp_url = {"jan": "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=1883644005&amp;format=interactive",
       "feb": "",
       "mar": "",
       "apr": "",
       "may": "",
       "jun": "",
       "jul": "",
       "aug": "",
       "sep": "",
       "oct": "",
       "nov": "",
       "dec": "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=1670414277&amp;format=interactive"}
text_month = {"jan": "January",
       "feb": "February",
       "mar": "March",
       "apr": "April",
       "may": "May",
       "jun": "June",
       "jul": "July",
       "aug": "August",
       "sep": "September",
       "oct": "October",
       "nov": "November",
       "dec": "December"}

# Create your views here.
def home(request):
    query = CustomUser.objects.all().filter(username=request.user)
    if len(query):
        return redirect('/profile/update')
    else:
        return redirect('/currency')
        #return render_to_response("index.html", RequestContext(request))
def climate(request, month):
    precip_src = precip_url[month]
    temp_src = temp_url[month]
    text = text_month[month]
    precip_chart_src = precip_chart_url[month]
    data = {"text_mon":text, "precip": precip_src, "precip_chart": precip_chart_src, "temp": temp_src}
    return render_to_response('climate.html', data, RequestContext(request))
def currency(request):
    chart = "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=1883251703&amp;format=interactive"
    map_five_chart = "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=489787441&amp;format=interactive"
    data = {"chart":chart, "map_five_chart":map_five_chart}
    return render_to_response('currency.html', data, RequestContext(request))
def ranking(request):
    data = {}
    preferences = []
    if request.POST.get('mybtn'):
        sum_total = 0
        for i in range(0, 12):
            print request.POST.get(str(i))
            sum_total += int(request.POST.get(str(i)))
            preferences.append(int(request.POST.get(str(i))))
            data["ranking"+str(i)] = request.POST.get(str(i))
        for i in range(0, 12):
          preferences[i] = float(preferences[i])/sum_total
        data["preferences"] = preferences
        query_countries = Country.objects.all()
        countries_display = []
        order = ["safety", "health", "internet", "travel", "openness", "price", "environment", "air", "ground", "tourist", "nature", "culture"]
        for country in query_countries:
          dict_country = model_to_dict(country)
          rank_list = []
          for criteria in order:
            rank_list.append(dict_country[criteria])
          multiplied = [float(a)*b for a,b in zip(preferences,rank_list)]
          ranking_final = sum(multiplied)
          dict_country["ranking"] = ranking_final
          print dict_country
          countries_display.append(dict_country)
        countries_display.sort(key=operator.itemgetter('ranking'), reverse=True)
        data["countries"] = countries_display
        print countries_display
    return render_to_response('rankings.html', data, RequestContext(request))


@login_required(login_url='/accounts/login')
def dash(request):
    return render_to_response('dashcontent.html', RequestContext(request))

@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def campaigns(request):
    user = CustomUser.objects.get(username=request.user)
    user_profile = user.get_user_profile()
    groups = Group.objects.all().filter(admin=request.user)
    data = {'profile_image': user_profile.profile_image_url(),
            'prof': user_profile, 'groups': groups, 'username': user}
    return render_to_response("groups.html", data, RequestContext(request))


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def update_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uplaoded_file(request.user, request.FILES['image_file'])
    return calupdate(request)


def compile_results(string1):
    print string1
