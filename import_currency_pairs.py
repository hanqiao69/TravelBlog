import csv
import json
from accounts.models import Currency, Country
from django.core.exceptions import ObjectDoesNotExist
import datetime
def populate():
   with open("currency_pairs_utf.csv", 'rU') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    skip = 0
    for row in file:
        if skip == 0:
            skip = 1
            continue
        country_code = row[0]
        currency_code = None
        name_curr = None
        if row[1] != "":
            currency_code = row[1]
        if row[2] != "":
            name_curr = row[2]
        if currency_code:
            currency_object = None
            try:
                currency_object = Currency.objects.get(code=currency_code)
            except ObjectDoesNotExist:
                continue
            currency_object.name=name_curr
            currency_object.save()
            country_object = None
            try: 
                country_object = Country.objects.get(code=country_code)
            except ObjectDoesNotExist:
                continue
            country_object.currency.add(currency_object)
            country_object.save()