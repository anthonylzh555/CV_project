import csv
import json

csvfile = open('20180308.csv', 'r')
jsonfile = open('20180308.json', 'w')

reader = csv.DictReader(csvfile)
out = json.dumps( [ row for row in reader ] )
jsonfile.write(out)
