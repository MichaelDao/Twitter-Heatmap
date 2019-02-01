# #Used to upload scraped data to the google storage

# from googleapiclient import discovery
# from oauth2client.client import GoogleCredentials

# credentials = GoogleCredentials.get_application_default()
# service = discovery.build('storage', 'v1', credentials=credentials)

# filename = 'tweetScrape.json'
# bucket = 'abgcorp-vicsafe'

# body = {'name': 'tweet_rawScrapejson'}
# req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
# resp = req.execute()