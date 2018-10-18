"""
Format the dataset and place it within the data folder.
"""

import csv
import json

all_data = []


import pprint


with open('../data/ted_main.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    header_title = None
    for row in csv_reader:
        if line_count <2 :
            header_title = row.copy()
            line_count += 1
        else:

            temp_dict = {}
            for i,col in enumerate(row):
                temp_dict[header_title[i]] = col
            all_data.append(temp_dict.copy())
            line_count+=1


with open('../data/transcripts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:

            for talk_dict in all_data:
                if talk_dict['url'] == row[1]:
                    talk_dict['transcript'] = row[0]
                    break
            line_count+=1


all_json = {}
for data in all_data:
    all_json[data['url'].strip()] = data



f = open("talks_data.json", "w")
f.write(json.dumps(all_json))
