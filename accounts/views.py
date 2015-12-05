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
# from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django.forms.models import model_to_dict
# from django.template import Context, Template
# from django.core import serializers
from accounts.models import CustomUser, Group, Country
import datetime
from django.contrib.auth.decorators import login_required
# from allauth.socialaccount.models import SocialToken
# from allauth.socialaccount.models import SocialAccount
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
number_month = {"jan": 0,
       "feb": 1,
       "mar": 2,
       "apr": 3,
       "may": 4,
       "jun": 5,
       "jul": 6,
       "aug": 7,
       "sep": 8,
       "oct": 9,
       "nov": 10,
       "dec": 11}
# Create your views here.
def home(request):
    #query = CustomUser.objects.all().filter(username=request.user)
    #if len(query):
    #    return redirect('/profile/update')
    #else:
  return redirect('/ranking')
        #return render_to_response("index.html", RequestContext(request))
def climate(request, month):
    temperature_data = "[['Country', 'Temperature (F)'],"
    rainfall_data = "[['Country', 'Rainfall (mm)'],"
    query_countries = Country.objects.all()
    countries = []
    for country in query_countries:
      dict_country = model_to_dict(country)
      temperature = json.loads(dict_country["temperature"])
      if temperature:
        temp_for_month = temperature[number_month[month]]
        dict_country["temp_for_month"] = temp_for_month
        if temp_for_month != "":
          temperature_data += '["'+dict_country["name"]+'",'+str(round(temp_for_month,2))+'],'
      rainfall = json.loads(dict_country["rainfall"])
      rainy_dry = json.loads(dict_country["rainy_dry"])
      if rainfall:
        rainfall_for_month = rainfall[number_month[month]]
        dict_country["rainfall_for_month"] = rainfall_for_month
        dict_country["rainy_dry_for_month"] = rainy_dry[number_month[month]]
        if rainfall_for_month != "":
          rainfall_data += '["'+dict_country["name"]+'",'+str(round(rainfall_for_month,2))+'],'
          countries.append(dict_country)
    temperature_data = temperature_data[:-1]+"]"
    rainfall_data = rainfall_data[:-1]+"]"
    text = text_month[month]
    data = {"text_mon":text, "rainfall_data":rainfall_data, "countries": countries, "temperature_data": temperature_data}
    return render_to_response('climate.html', data, RequestContext(request))
def currency(request):
    currency_data = "[['Country', 'Percentage Change'],"
    query_countries = Country.objects.all()
    countries = []
    for country in query_countries:
      dict_country = model_to_dict(country)
      currency = country.currency.all()
      if currency != None and len(currency)>0:
        currency = currency[0]
        dict_country["currency"] = currency
        if currency.percent_change != None:
          negative = ""
          if currency.percent_change < 0:
            negative = "-"
          currency_data += '["'+dict_country["name"]+'",'+negative+str(abs(round(currency.percent_change*100,2)))+'],'
      countries.append(dict_country)
    currency_data = currency_data[:-1]+"]"
    map_five_chart = "https://docs.google.com/spreadsheets/d/1ETe5bXdUNtejhv9Axph4fKl94p6g2vysDMDgH0JY_B4/pubchart?oid=489787441&amp;format=interactive"
    data = {"countries":countries, "currency_data":currency_data}
    return render_to_response('currency.html', data, RequestContext(request))
def country(request, country_code):
    country = None
    try:
      country = Country.objects.get(code=country_code)
    except ObjectDoesNotExist:
        return redirect('/ranking')
    dict_country = model_to_dict(country)
    list_metrics = []
    order = ["safety", "price", "nature", "culture", "environment", "air", "ground", "tourist", "health", "internet", "travel", "openness", ]
    name = ["Safety", "Price", "Natural Life", "Cultural Resources", "Env. Sustainability", "Air Infrastructure", "Ground Infrastructure", "Tourism Infrastructure", "Healthcare", "Internet", "Gov't Focus on Tourism", "Int'l Openness"]
    colors = ["#c12323", "#d3d42a", "#6cd443", "#2ca4a7", "#911fc5", "#f2798f", "#d977bf", "#263f73", "#3c5fa6", "#85f2f2", "#dddddd", "#449edd"]
    string = ""
    metrics_2 = '{label:"World Economic Forum Rankings", fillColor: "rgba(151,187,205,0.5)", strokeColor: "rgba(151,187,205,0.8)", highlightFill: "rgba(151,187,205,0.75)", highlightStroke: "rgba(151,187,205,1)", data: ['
    temperature = '{label:"Temperature (F)", fillColor: "rgba(220,220,220,0.2)", strokeColor: "rgba(220,220,220,1)", pointColor: "rgba(220,220,220,1)", pointStrokeColor: "#fff", pointHighlightFill: "#fff", pointHighlightStroke: "rgba(220,220,220,1)", data: ['
    rainfall = '{label:"Rainfall (mm)", fillColor: "rgba(151,187,205,0.2)", strokeColor: "rgba(151,187,205,1)", pointColor: "rgba(151,187,205,1)", pointStrokeColor: "#fff", pointHighlightFill: "#fff", pointHighlightStroke: "rgba(151,187,205,1)", data: ['
    if dict_country["safety"] != None:
      for i, criteria in enumerate(order):
        string += '{value:'+str(round(float(dict_country[criteria]), 2))+', color: "'+colors[i]+'", label: "'+name[i]+'"},'
        metrics_2 += str(round(float(dict_country[criteria]), 2))+","
      metrics_2 = metrics_2[:-1] + "]}"
    else:
      string = None
      metrics_2 = None
    temperature_list = json.loads(dict_country["temperature"])
    for i, temp in enumerate(temperature_list):
      if i < 12 and temp!="":
          temperature += str(round(float(temp), 2))+","
      else:
        temperature += " "
    rainfall_list = json.loads(dict_country["rainfall"])
    for i, rain in enumerate(rainfall_list):
      if i < 12 and temp!="":
        rainfall += str(round(float(rain), 2))+","
      else:
        rainfall += " "
    temperature = temperature[:-1]+"]}"
    rainfall = rainfall[:-1]+"]}"

    #get currency data
    currency = country.currency.all()
    dict_currency = None
    if currency != None:
      currency = currency[0]
      dict_currency = model_to_dict(currency)
      dict_currency["url"] = "https://www.google.com/finance/chart?es_sm=119&q=CURRENCY:USD"+currency.code+"&tkr=1&p=5Y&chst=vkc&chs=500x300&chsc=1&ei=K2U2VpilKouvetuxrpgF"
    data = {"country": dict_country, "dict_currency": dict_currency, "metrics": string, "metrics_2": metrics_2, "labels": name, "temperature": temperature, "rainfall": rainfall}
    return render_to_response('country.html', data, RequestContext(request))
def ranking(request):
    data = {}
    preferences = []
    for i in range(0, 12):
            data["ranking"+str(i)] = 0
            data["selected_11"] = "selected"
    if request.method == 'GET':
      if "search_query" in request.session:
        data = ast.literal_eval(request.session["search_query"])
        loaded_data = True
    if request.POST.get('mybtn'):
        print request.POST
        print request.POST.get("month")
        print request.POST.get("temp")
        print request.POST.get("rainfall")
        print request.POST
        if request.POST.get("month"):
          month_gotten = int(request.POST.get("month"))
          data["month"] = month_gotten
          for i in range(0, 12):
            if i == month_gotten:
              data["selected_"+str(i)] = "selected"
            else:
              data["selected_"+str(i)] = ""

        if request.POST.get("temp"):
          data[request.POST.get("temp")+"_checked"] = "checked"
          data["temp_saved"] = True
        if request.POST.get("rainfall"):
          data[request.POST.get("rainfall")+"_checked"] = "checked"
          data["rainfall_saved"] = True
        saved_data = ["above_temp", "below_temp", "between_low_temp", "between_high_temp"]
        for saved_attribute in saved_data:
          data[saved_attribute+"_saved"] = request.POST.get(saved_attribute)
        sum_total = 0
        for i in range(0, 12):
            print request.POST.get(str(i))
            sum_total += int(request.POST.get(str(i)))
            preferences.append(int(request.POST.get(str(i))))
            data["ranking"+str(i)] = int(request.POST.get(str(i)))
        #save in user search cache
        inv_month = dict(zip(number_month.values(), number_month.keys()))
        data["short_name"] = "Travel in: " + inv_month[int(request.POST.get("month"))] + " at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print request.user
        if request.user.is_authenticated():
          user = CustomUser.objects.get(username=request.user)
          user_profile = user.get_user_profile()
          if user_profile.search_cache:
            existing_cache = json.loads(user_profile.search_cache)
            if len(existing_cache) > 10:
              existing_cache.pop()
            existing_cache.insert(0, data)
            user_profile.search_cache = json.dumps(existing_cache)
            user_profile.save()
          else:
            search_cache = []
            search_cache.insert(0, data)
            user_profile.search_cache = json.dumps(search_cache)
            user_profile.save()
        request.session["search_query"] = str(data)
        if sum_total == 0:
          sum_total += 1
        for i in range(0, 12):
          preferences[i] = float(preferences[i])/sum_total
        data["preferences"] = preferences
        query_countries = Country.objects.all()
        countries_display = []
        order = ["safety", "health", "internet", "travel", "openness", "price", "environment", "air", "ground", "tourist", "nature", "culture"]
        for country in query_countries:
          #temporary to fix incomplete datasets
          dict_country = model_to_dict(country)
          if dict_country["safety"] == None:
            continue
          rank_list = []
          for criteria in order:
            rank_list.append(dict_country[criteria])
          multiplied = [float(a)*b for a,b in zip(preferences,rank_list)]
          ranking_final = sum(multiplied)
          dict_country["ranking"] = ranking_final
          #print dict_country

          #REMOVE BASED ON RAINFALL FIELD
          exclude = False
          if request.POST.get("temp"):
            temperature = json.loads(dict_country["temperature"])
            temp_for_month = temperature[int(request.POST.get("month"))]
            dict_country["temp_for_month"] = temp_for_month
            if temp_for_month == "":
              pass
            else:
              if request.POST.get("temp") == "below":
                below_temp = request.POST.get("below_temp")
                if float(temp_for_month) > float(below_temp):
                  exclude = True
              if request.POST.get("temp") == "above":
                above_temp = request.POST.get("above_temp")
                if float(temp_for_month) < float(above_temp):
                  exclude = True
              if request.POST.get("temp") == "between":
                low_temp = request.POST.get("between_low_temp")
                high_temp = request.POST.get("between_high_temp")
                if float(temp_for_month) < float(low_temp) or float(temp_for_month) > float(high_temp):
                  exclude = True
          if request.POST.get("rainfall"):
            rainy_dry = json.loads(dict_country["rainy_dry"])
            rainy_dry_for_month = rainy_dry[int(request.POST.get("month"))] 
            dict_country["rainy_dry_for_month"] = rainy_dry_for_month
            if rainy_dry_for_month == "":
              pass
            else:
              if request.POST.get("rainfall") == "dry" or request.POST.get("rainfall") == "wet":
                if rainy_dry_for_month != "" and rainy_dry_for_month != capitalize_rain(request.POST.get("rainfall")):
                  exclude = True
          if exclude != True:
            countries_display.append(dict_country)
        countries_display.sort(key=operator.itemgetter('ranking'), reverse=True)
        data["countries"] = countries_display
        #print countries_display
    return render_to_response('rankings.html', data, RequestContext(request))

def capitalize_rain(rainfall):
  if rainfall == "dry":
    return "Dry"
  if rainfall == "wet":
    return "Rainy"

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

