from google.cloud import bigquery
client = bigquery.Client()
dataset_id = 'tweet_hashtag'
dataset_ref = client.dataset(dataset_id)
job_config = bigquery.LoadJobConfig()
job_config.autodetect = True
job_config.skip_leading_rows = 1

# The source format defaults to CSV, so the line below is optional.
#uri = 'gs://abgcorp-vicsafe/ImpeachTrump.csv'

#Where we define the Schema of the table
schema = [
    bigquery.SchemaField('user_id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('latitude', 'FLOAT', mode='REQUIRED'),
    bigquery.SchemaField('tweet_id', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('longitude', 'FLOAT', mode='REQUIRED'),
]

#create table in BigQuery
table_ref = dataset_ref.table('ImpeachTrump')
table = bigquery.Table(table_ref, schema)
table = client.create_table(table)  # API request

assert table.table_id == 'ImpeachTrump'

# load_job = client.load_table_from_uri(
#     uri,
#     dataset_ref.table('ImpeachTrump'),
#     job_config=job_config)  # API request
# print('Starting job {}'.format(load_job.job_id))

# load_job.result()  # Waits for table load to complete.
# print('Job finished.')


# destination_table = client.get_table(dataset_ref.table('ImpeachTrump'))
# print('Loaded {} rows.'.format(destination_table.num_rows))