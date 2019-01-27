from google.cloud import bigquery

client = bigquery.Client()

query_job = client.query("""
  SELECT * FROM `vic_crime.suburb`
  WHERE Year_ending_September = 2010
   """)

results = query_job.result()  # Waits for job to complete.

for row in results: print("{}".format(row.Year_ending_September) )

