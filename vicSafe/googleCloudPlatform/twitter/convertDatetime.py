# -*- coding: utf-8 -*-:
import json

fname = 'tweetScrape.json'

with open(fname, 'r') as f:


    # Prepare counters
    all_users = []
    total_tweets = 0
    geo_tweets = 0

    # Loop through each line in our raw file
    # for line in f:
    #     tweet = json.loads(line)

    #     time = tweet['created_at']
    #     yeet = tweet['text']
    #     print(time)
    #     print(yeet)

    #!/usr/bin/python
import time

struct_time = time.strptime("30 Nov 00", "%d %b %y")
print ("returned tuple: " )
print (struct_time)
