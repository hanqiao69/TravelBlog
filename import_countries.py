import csv
from accounts.models import Country
def populate():
   with open("countries_utf.csv", 'rU') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    skip = 0
    for row in file:
    	if skip == 0:
    		skip = 1
    		continue
    	for index, value in enumerate(row):
    		if index >1:
    			row[index] = float(row[index])
    	country = Country.objects.get_or_create(code=str(row[0]), name=str(row[1]), safety=row[2], health=row[3], internet=row[4], travel=row[5], openness=row[6],price=row[7], environment=row[8], air=row[9], ground=row[10], tourist=row[11], nature=row[12], culture=row[13])
