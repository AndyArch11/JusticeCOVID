import csv
import json

csv_prison_file = './Prison Map/data/prison_list.csv'
json_prison_file = './Prison Map/data/prison_list.json'

data = []
with open (csv_prison_file) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        if 'Operational' in csvRow['Status']:
            data.append(csvRow)

with open(json_prison_file, "w") as jsonFile:
    jsonFile.write(json.dumps(data, indent = 4))