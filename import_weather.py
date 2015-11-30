import csv
import json
from accounts.models import Country
def populate():
   with open("weather_utf.csv", 'rU') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    skip = 0
    for row in file:
        if skip == 0:
            skip = 1
            continue
        list_temp = []
        list_rainfall = []
        list_wet_dry = []
        for index, value in enumerate(row):
            if index > 0:
                if row[index] != "" and row[index] != "Rainy" and row[index] != "Dry":
                    row[index] = float(row[index])  
            if index >=1 and index < 14:
                list_temp.append(row[index])
            if index >= 14 and index < 27:
                list_rainfall.append(row[index])
            if index >= 27:
                list_wet_dry.append(row[index])
        print json.dumps(list_temp)
        print json.dumps(list_rainfall)
        print json.dumps(list_wet_dry)
        country = Country.objects.update_or_create(code=str(row[0]), defaults={'temperature':json.dumps(list_temp), 'rainfall':json.dumps(list_rainfall), 'rainy_dry':json.dumps(list_wet_dry)})
