import csv
import json
from accounts.models import Currency
import datetime
def populate():
   with open("currency_import_utf.csv", 'rU') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    skip = 0
    for row in file:
        if skip == 0:
            skip = 1
            continue
        code = row[0]
        current = None
        average = None
        percentage = None
        if row[1] != "":
            current = float(row[1])
        if row[2] != "":
            average = float(row[2])
        if current and average and average != 0:
            percentage = (current - average)/average
        country = Currency.objects.update_or_create(code=str(row[0]), defaults={'current':current, 'five_yr_mean':average, 'percent_change':percentage, 'current_updated': datetime.date.today()})