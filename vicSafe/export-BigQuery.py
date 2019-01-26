from google.cloud import bigquery
client = bigquery.Client()
bucket_name = 'abgcorp-vicsafe'
project = 'bigquery-public-data.stackoverflow.posts_questions'
dataset_id = 'samples'
table_id = 'shakespeare'

destination_uri = 'gs://{}/{}'.format(bucket_name, 'shakespeare.csv')
dataset_ref = client.dataset(dataset_id, project=project)
table_ref = dataset_ref.table(table_id)

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location='US')  # API request
extract_job.result()  # Waits for job to complete.

print('Exported {}:{}.{} to {}'.format(
    project, dataset_id, table_id, destination_uri))