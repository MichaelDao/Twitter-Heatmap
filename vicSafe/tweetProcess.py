# -*- coding: utf-8 -*-:
import json
import geocoder

# Tweets are stored in in file "fname". In the file used for this script,
# each tweet was stored on one line
fname = 'tweetScrape.json'
outname = 'tweetProcess.json'
geoCodeKey = 'Z3Xd2SCGcM9fiaoKnm18ZhI09X0Z0Hw3'

# find geolocation with mapquest
def findGeoFunc(location):
    # get longitutde and latitude with location query
    geoCode = geocoder.mapquest(location, key=geoCodeKey)
    latitude = geoCode.lat
    longitute = geoCode.lng

    # Log to console
    print(str(location) + "\n Latitude:" + str(latitude) + " Longitude:" + str(longitute) + '\n')

    # save to array
    # coordArray = [latitude, longitute]
    return ([latitude, longitute])


with open(fname, 'r') as f:
    # Create dictionary to later be stored as JSON. All data will be included
    # in the list 'data'
    users_with_geodata = {
        "data": []
    }

    all_users = []
    total_tweets = 0
    geo_tweets = 0

    # Loop through each line in our raw file
    for line in f:
        tweet = json.loads(line)

        # if the tweet has a user id, analyse
        if tweet['user']['id']:
            total_tweets += 1
            user_id = tweet['user']['id']
            if user_id not in all_users:

                # only find coordinates if location exists
                locationString = tweet['user']['location']
		
		print (locationString)


                if locationString is not None:
                    locationString.encode('utf-8').strip()
		    print (locationString)
		    try:
		        coord = findGeoFunc(locationString)
		    except:
			print("there was an error")

                    all_users.append(user_id)

                    # Give users some data to find them by. User_id listed separately
                    # to make iterating this data later easier
                    user_data = {
                        "user_id": tweet['user']['id'],
                        "tweet_id": tweet['id'],
                        #"location": tweet['user']['location'],
                        "longitude": coord[0],
                        "latitude": coord[1],
                    }

                # Add only tweets with some geo data to .json. Comment this if you want to include all tweets.
                if tweet['user']['location']:
                    users_with_geodata['data'].append(user_data)
                    geo_tweets += 1

            # If user already listed, increase their tweet count
            elif user_id in all_users:
                for user in users_with_geodata["data"]:
                    if user_id == user["user_id"]:
                        print ('') 
			#user["tweets"] += 1

    # Get some aggregated numbers on the data
    # print("The file included " + str(len(all_users)) +
    #       " unique users who tweeted with or without geo data")

    print("The file included " + str(len(users_with_geodata['data'])) +
          " unique users who tweeted with geo data")

# Save data to JSON file
with open(outname, 'w') as fout:
    fout.write(json.dumps(users_with_geodata, indent=4))
