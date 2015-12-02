import csv
import json
from accounts.models import Country
def populate():
   with open("fix_names_utf.csv", 'rU') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    skip = 0
    for row in file:
        if skip == 0:
            skip = 1
            continue
        name = row[0]
        country = Country.objects.update_or_create(code=str(row[1]), defaults={'name':name})
