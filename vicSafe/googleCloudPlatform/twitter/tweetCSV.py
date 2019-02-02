# -*- coding: utf-8 -*-
import json
import csv

## This is redundant, but will leave it here as it is
## a way for us to manually process the JSON file 
## into csv data once the whole JSON is dumped

# The json file that we doesnt have any nested data
fname = "tweetProcess.json"
outname = "manual.csv"

with open(fname, encoding='utf-8') as file:
    data = json.load(file)

with open(outname, "w") as file:
    csv_file = csv.writer(file)

    # The whole json file
    for item in data.values():

        first = True # boolean to make a special case for the first column

        # Create header
        for key,value in item[0].items():
            # special first case
            if first:
                first = False
                file.write(str(key))
            else:
                file.write("," + str(key))

        file.write("\n") # new line
        first = True # reset boolean

        # Iterate through the rest of the data
        for item in item:
            # each item in the line
            for key,value in item.items():
                # special first case
                if first:
                    first = False
                    file.write(str(value))

                else:
                    file.write("," + str(value))

            # new line
            file.write("\n")
            first = True # reset boolean

    # just to log something
    print('CSV file "' + outname +'" created')