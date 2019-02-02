# -*- coding: utf-8 -*-:
import json
import geocoder
import csv

# Tweets are stored in in file "fname". In the file used for this script,
# each tweet was stored on one line
fname = 'tweetScrape.json'
outname = 'tweetProcess.json'
geoCodeKey = 'Z3Xd2SCGcM9fiaoKnm18ZhI09X0Z0Hw3'

# The json  file variable names
csvName = "ready.csv"

# find geolocation with mapquest

def findGeoFunc(location):
    # get longitutde and latitude with location query
    geoCode = geocoder.mapquest(location, key=geoCodeKey)
    latitude = geoCode.lat
    longitute = geoCode.lng

    # Log to console
    print(str(location) + "\n Latitude:" + str(latitude) + " Longitude:" + str(longitute) + '\n')

    # return as array
    return ([latitude, longitute])

# Check if the CSV already exists, if it does then prepare our header
def prepareCSV(user_data):
    try:
        # File already exists
        fCheck = open(csvName, 'r')
        fCheck.close()

    except FileNotFoundError:
        # Keep preset values file not found
        print('Creating new file \n')

        # Open a new file
        newFile = open(csvName, "w+")

        # first line is unfortunately hardcoded header
        newFile.write("time,user_id,tweet_id,longitude,latitude,favourites\n")
        newFile.close()
        

    addLine = open(csvName, 'a')

    tweetCSVLine = user_data['time'] + ',' + str(user_data['user_id']) + ',' + str(user_data['tweet_id']) + \
        ',' + str(user_data['longitude']) + ',' + str(user_data['latitude']) + ',' + str(user_data['favourites']) + '\n'


    addLine.write(tweetCSVLine)


with open(fname, 'r') as f:

    # Create dictionary to later be stored as JSON. All data will be included
    # in the list 'data'
    users_with_geodata = {
        "data": []
    }

    # Prepare counters
    all_users = []
    total_tweets = 0
    geo_tweets = 0

    # Loop through each line in our raw file
    for line in f:
        tweet = json.loads(line)

        # if the tweet has a user id, analyse
        if tweet['user']['id']:

            # Increment total tweeets
            total_tweets += 1
            print('analysing tweet ' + str(total_tweets) + '\n')

            # Prepare user ID and make sure it is distinct
            user_id = tweet['user']['id']
            if user_id not in all_users:

                # only find coordinates if location exists
                locationString = tweet['user']['location']

                # Location is not null
                if locationString is not None:

                    # Attempt at unicode bugfix, use try catch if continues
                    locationString.encode('utf-8').strip()
                    coord = findGeoFunc(locationString)

                    # add this gelocated user to list
                    all_users.append(user_id)

                    # Give users some data to find them by. User_id listed separately
                    # to make iterating this data later easier
                    user_data = {
                        "time": tweet['created_at'],
                        "user_id": tweet['user']['id'],
                        "tweet_id": tweet['id'],
                        "longitude": coord[0],
                        "latitude": coord[1],
                        "favourites": tweet['user']['favourites_count'],
                    }
                    prepareCSV(user_data)  # prepare CSV file for saving

                # Add only tweets with some geo data to .json.
                # Also focus on solely the location for counter
                if tweet['user']['location']:
                    users_with_geodata['data'].append(user_data)
                    geo_tweets += 1

    # how many of our users have geodata?
    print("The file included " + str(len(users_with_geodata['data'])) +
          " unique users who tweeted with geo data")

# Save data to JSON file at the end of the process
with open(outname, 'w') as fout:
    fout.write(json.dumps(users_with_geodata, indent=4))
