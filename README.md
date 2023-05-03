# Import Superset Dashboard Action

This action imports a dashboard from local path ZIP file to Superset
This action expects to have 2 additional environment variables inside the workflow

1. `SUPERSET_USERNAME`
2. `SUPERSET_PASSWORD`

## Inputs
### `url_base`
**Required** Base URL for your Superset API endpoint. Default: `http://localhost:8088`

### `dashboard_file_path`
**Required** Path of the dashboard you want to import. 

## Example usage
```
uses: actions/import-superset-dashboard-action@v1
with:
  url-base: http://localhost:8088
  dashboard_file_path: dashboard.zip
```

## Example Workflow
```
name: Example Workflow for importing Superset dashboard

on:
  push:
    branches:
      - master

env:
  SUPERSET_USERNAME: test
  SUPERSET_PASSWORD: testpass

jobs:
  uses: actions/import-superset-dashboard-action@v1
  with:
    url-base: http://localhost:8088
    dashboard_file_path: dashboard.zip
```