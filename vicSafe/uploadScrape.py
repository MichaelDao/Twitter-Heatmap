#from googleapiclient import discovery
#from oauth2client.client import GoogleCredentials

#credentials = GoogleCredentials.get_application_default()
#service = discovery.build('storage', 'v1', credentials=credentials)

#filename = 'tweetScrape.json'
#bucket = 'abgcorp-vicsafe'

#body = {'name': 'metoo_2.json'}
#req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
#resp = req.execute()

from google.cloud import storage

client = storage.Client(project='project-xxx')
bucket = client.get_bucket('bucket-xxx')
blob = bucket.blob('test.txt')
blob.upload_from_filename('test.txt')