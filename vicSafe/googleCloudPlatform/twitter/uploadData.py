#from googleapiclient import discovery
#from oauth2client.client import GoogleCredentials

#credentials = GoogleCredentials.get_application_default()
#service = discovery.build('storage', 'v1', credentials=credentials)

#filename = 'tweetScrape.json'
#bucket = 'abgcorp-vicsafe'

#body = {'name': 'metoo_2.json'}
#req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
#resp = req.execute()

#Alternative to uploadData-Bucket

from google.cloud import storage

client = storage.Client(project='abgcorp-vicsafe')
bucket = client.get_bucket('abgcorp-vicsafe')

uploadData = input("Save the file as?")
fileData = input("Enter in name of file you want to upload (local)")

blob = bucket.blob(uploadData + '.csv')
blob.upload_from_filename('data/'+ fileData+ '.csv')