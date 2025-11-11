# Data Ingestion Pipeline

This pipeline automates the ingestion of data into Vertex AI Search, streamlining the process of building Retrieval Augmented Generation (RAG) applications.

It orchestrates the complete workflow: loading data, chunking it into manageable segments, generating embeddings using Vertex AI Embeddings, and importing the processed data into your Vertex AI Search datastore.

You can trigger the pipeline for an initial data load or schedule it to run periodically, ensuring your search index remains current. Vertex AI Pipelines provides the orchestration and monitoring capabilities for this process.

## Prerequisites

Before running any commands, ensure you have set your Google Cloud Project ID as an environment variable. This variable will be used by the subsequent `make` commands.

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
```
Replace `"YOUR_PROJECT_ID"` with your actual Google Cloud Project ID.

Now, you can set up the development environment:

1.  **Set up Dev Environment:** Use the following command from the root of the repository to provision the necessary resources in your development environment using Terraform. This includes deploying a datastore and configuring the required permissions.

    ```bash
    make setup-dev-env
    ```
    This command requires `terraform` to be installed and configured.

## Running the Data Ingestion Pipeline

After setting up the infrastructure using `make setup-dev-env`, you can run the data ingestion pipeline.

> **Note:** The initial pipeline execution might take longer as your project is configured for Vertex AI Pipelines.

**Steps:**

**a. Execute the Pipeline:**
Run the following command from the root of the repository. Ensure the `PROJECT_ID` environment variable is still set in your current shell session (as configured in Prerequisites).

```bash
make data-ingestion
```

This command handles installing dependencies (if needed via `make install`) and submits the pipeline job using the configuration derived from your project setup. The specific parameters passed to the underlying script depend on the `datastore_type` selected during project generation:
*   It will use parameters like `--data-store-id`, `--data-store-region`.
*   Common parameters include `--project-id`, `--region`, `--service-account`, `--pipeline-root`, and `--pipeline-name`.

**b. Pipeline Scheduling:**

The `make data-ingestion` command triggers an immediate pipeline run. For production environments, the underlying `submit_pipeline.py` script also supports scheduling options with flags like `--schedule-only` and `--cron-schedule` for periodic execution.

**c. Monitoring Pipeline Progress:**

The pipeline's configuration and execution status link will be printed to the console upon submission. For detailed monitoring, use the Vertex AI Pipelines dashboard in the Google Cloud Console.

## Testing Your RAG Application

Once the data ingestion pipeline completes successfully, you can test your RAG application with Vertex AI Search.
> **Troubleshooting:** If you encounter the error `"google.api_core.exceptions.InvalidArgument: 400 The embedding field path: embedding not found in schema"` after the initial data ingestion, wait a few minutes and try again. This delay allows Vertex AI Search to fully index the ingested data.