import tweepy
from tweepy import Stream
from tweepy import StreamListener
from tweepy import OAuthHandler
import json

# Input credentials here
consumer_key = 'OmeZsCXuwit2lBoUsUvq2Sh1J'
consumer_secret = 'EbCgWSOZIQuPNzlMSKlkFCWlzi2YWgsfNaQSVzUkUpd8fy3agb'
access_token = '213604793-gVLy2CqhXZj7Dcf7BmipdU4jlo69Y2Kc0X4mm4Pv'
access_token_secret = 'Q0PhebdRElh3uYH04yvzuV6mjVfp4WtUTJ0mTcsKyZnNo'

# setup credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# authenticate API
api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

counter = 0 # counter to check how many tweets are downloaded so far
fname = 'tweetScrape.json'
hashtag = '#metoo'

# Stream tweets
class MyListener(StreamListener):   
    print ('\nWill print out tweet data to ' + fname + ' under hashtag ' + hashtag + '\n') 

    def on_data(self, data):
        try:
            with open(fname, 'a') as f:
                # write to csv
                f.write(data)

                # Log the tweets downloaded
                global counter
                counter += 1
                print('Tweet no. ' + str(counter) + ' downloaded\n')

                return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# Set the hashtag to be searched
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=[hashtag])