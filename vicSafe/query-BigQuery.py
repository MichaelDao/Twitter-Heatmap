from google.cloud import bigquery

client = bigquery.Client()

query_job = client.query("""
  SELECT longitude, latitude FROM `tweet_hashtag.metoo`
   """)

results = query_job.result()  # Waits for job to complete.

for row in results: print("{} : {}".format(row.longitude, row.latitude) )

