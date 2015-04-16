# Combine the following zip code databases and output as a single csv:
#
# From http://geocoder.ca/?freedata=1 : zip5.csv and Canada.csv
# From http://www.boutell.com/zipcodes/ : zipcode.csv
#
# Known bug: The Canadian data contains non-ASCII characters that don't end
# up encoded properly.

import csv
import string
import sys


print "zip,city,state,latitude,longitude"

zipdata = {}

with open("zipcode.csv", "r") as zipfile:
    csvreader = csv.DictReader(zipfile)
    for row in csvreader:
        zipdata[row["zip"]] = ( row["city"], row["state"], float(row["latitude"]), float(row["longitude"]) )

with open("zip5.csv", "r") as zipfile:
    csvreader = csv.DictReader(zipfile, fieldnames=("zip","city","state","latitude","longitude","county"))
    for row in csvreader:
        if not row["zip"] in zipdata:
            zipdata[row["zip"]] = ( row["city"], row["state"], float(row["latitude"]), float(row["longitude"]) )

with open("Canada.csv", "r") as postfile:
    csvreader = csv.DictReader(postfile)
    for row in csvreader:
        city = row["city"].upper().replace(",","")
        city = string.replace(city, "&#39;", "'")
        zipdata[row["postcode"]] = ( city, row["province"], float(row["latitude"]), float(row["longitude"]) )

for k,v in zipdata.iteritems():
    print ",".join([ k, v[0].upper(), v[1], str(v[2]), str(v[3]) ])

