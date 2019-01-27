from google.cloud import bigquery
client = bigquery.Client()
bucket_name = 'abgcorp-vicsafe'
project = 'abgcorp-vicsafe'
dataset_id = 'vic_crime'
table_id = 'suburb'

destination_uri = 'gs://{}/{}'.format(bucket_name, 'results.csv')
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