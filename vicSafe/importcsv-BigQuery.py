from google.cloud import bigquery
client = bigquery.Client()
dataset_id = 'tweet_hashtag'

dataset_ref = client.dataset(dataset_id)
job_config = bigquery.LoadJobConfig()
job_config.autodetect = True
job_config.skip_leading_rows = 1
# The source format defaults to CSV, so the line below is optional.
uri = 'gs://abgcorp-vicsafe/metoo.csv'

table_ref = dataset_ref.table('metoo')
table = bigquery.Table(table_ref)
# table = client.create_table(table)  # API request

assert table.table_id == 'metoo'

load_job = client.load_table_from_uri(
    uri,
    dataset_ref.table('metoo'),
    job_config=job_config)  # API request
print('Starting job {}'.format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print('Job finished.')

destination_table = client.get_table(dataset_ref.table('metoo'))
print('Loaded {} rows.'.format(destination_table.num_rows))