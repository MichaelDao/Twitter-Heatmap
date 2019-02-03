# -*- coding: utf-8 -*-:
import geocoder
import csv

import tweepy
from tweepy import Stream
from tweepy import StreamListener
from tweepy import OAuthHandler
import json

counterTweet = 0

# Input credentials here
consumer_key = 'OmeZsCXuwit2lBoUsUvq2Sh1J'
consumer_secret = 'EbCgWSOZIQuPNzlMSKlkFCWlzi2YWgsfNaQSVzUkUpd8fy3agb'
access_token = '213604793-gVLy2CqhXZj7Dcf7BmipdU4jlo69Y2Kc0X4mm4Pv'
access_token_secret = 'Q0PhebdRElh3uYH04yvzuV6mjVfp4WtUTJ0mTcsKyZnNo'
geoCodeKey = 'Z3Xd2SCGcM9fiaoKnm18ZhI09X0Z0Hw3'

# setup credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# authenticate API
api = tweepy.API(auth)


def scrape(hashtagSearch):
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status

    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse

    #hashtagSearch = input("Enter in the hashtag you want to Scrape: ")
    fname = "data/" + hashtagSearch + "_raw.json"
    hashtag = "#" + hashtagSearch

    try:
        class MyListener(StreamListener):

            print('\nWill print out tweet data to ' + fname + ' under hashtag ' + hashtag + '\n')

            def on_data(self, data):

                try:
                    with open(fname, 'a') as f:
                        # write to csv
                        f.write(data)

                        # Log the tweets downloaded
                        global counterTweet
                        counterTweet += 1

                        print('Tweet no. ' + str(counterTweet) + ' downloaded\n')

                        if (counterTweet == 2):
                            print('we have reached our limit')
                            return False

                        return True

                except BaseException as e:
                    # attempt to make this as input
                    print("Error on_data: %s" % str(e))
                return True

            def on_error(self, status):
                print(status)
                return True

        # Set the hashtag to be searched
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=[hashtag])

    except KeyboardInterrupt:
        print("stopping the process manually")

    return


def process(fnameInput):
    # Tweets are stored in in file "fname". In the file used for this script,
    # each tweet was stored on one line
    #fnameInput = input("Enter Filename of Scrape to Process:")

    fname = 'data/' + fnameInput + '_raw.json'
    outName = 'data/' + fnameInput + '_ready'

    # Wrapped in a try catch to help process json file on interrupt
    try:
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
                fCheck = open(outName + '.csv', 'r')
                fCheck.close()

            except FileNotFoundError:
                # Open a new file
                newFile = open(outName + '.csv', "w+")

                first = True

                # Create header
                for key, value in user_data.items():
                    # special first case
                    if first:
                        first = False
                        newFile.write(str(key))
                    else:
                        newFile.write("," + str(key))

                # New line and close header writing
                newFile.write('\n')
                newFile.close()

            addLine = open(outName + '.csv', 'a')

            # Create header
            first = True

            for key, value in user_data.items():
                # special first case
                if first:
                    first = False
                    addLine.write(str(value))
                else:
                    addLine.write("," + str(value))

            # tweetCSVLine =  str(user_data['user_id']) + ',' + str(user_data['tweet_id']) + \
                # ',' + str(user_data['longitude']) + ',' + str(user_data['latitude']) + ',' + str(user_data['favourites']) + '\n'

            # addLine.write(tweetCSVLine)
            addLine.close()

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
                                # "time": tweet['created_at'],
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
            print("The file included " + str(len(users_with_geodata['data']))
                  + " unique users who tweeted with geo data")

        # Save data to JSON file at the end of the process
        with open(outName + '.json', 'w') as fout:
            fout.write(json.dumps(users_with_geodata, indent=4))

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, Creating unfinished JSON file")
        with open(outName + '.json', 'w') as fout:
            fout.write(json.dumps(users_with_geodata, indent=4))


# START FROM HERE
import sys
print ("This is the name of the script: " + sys.argv[1] + " " + sys.argv[2])

hashInput = input("Enter in the hashtag you want to Scrape: ")
# scrape the data 
scrape(hashInput)

# process the location
process(hashInput)

# process the time

# upload both

