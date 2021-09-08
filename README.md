# GHBQ

## Workflow

1. Generate a BigQuery with `ghbq-generate`

2. Run the query on https://console.cloud.google.com/bigquery

3. Download the results as `<name>.csv` and save the job information as `<name>.job`

    - Sample files with `ghbq-sample` (Creates `<name>.<size>.csv`)

    - Split dataset with `ghbq-split` (Creates `<name>.a.csv` and `<name>.b.csv`)

4. Download files with `ghbq-download`
