# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ruff: noqa

from kfp.dsl import Dataset, Input, component


@component(
    base_image="us-docker.pkg.dev/production-ai-template/starter-pack/data_processing:0.2"
)
def ingest_data(
    project_id: str,
    data_store_region: str,
    input_files: Input[Dataset],
    data_store_id: str,
    embedding_dimension: int = 768,
    embedding_column: str = "embedding",
) -> None:
    """Process and ingest documents into Vertex AI Search datastore.

    Args:
        project_id: Google Cloud project ID
        data_store_region: Region for Vertex AI Search
        input_files: Input dataset containing documents
        data_store_id: ID of target datastore
        embedding_column: Name of embedding column in schema
    """
    import json
    import logging
    import time

    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    def update_schema_as_json(
        original_schema: str,
        embedding_dimension: int,
        field_name: str | None = None,
    ) -> str:
        """Update datastore schema JSON to include embedding field.

        Args:
            original_schema: Original schema JSON string
            field_name: Name of embedding field to add

        Returns:
            Updated schema JSON string
        """
        original_schema_dict = json.loads(original_schema)

        if original_schema_dict.get("properties") is None:
            original_schema_dict["properties"] = {}

        if field_name:
            field_schema = {
                "type": "array",
                "keyPropertyMapping": "embedding_vector",
                "dimension": embedding_dimension,
                "items": {"type": "number"},
            }
            original_schema_dict["properties"][field_name] = field_schema

        return json.dumps(original_schema_dict)

    def update_data_store_schema(
        project_id: str,
        location: str,
        data_store_id: str,
        field_name: str | None = None,
        client_options: ClientOptions | None = None,
    ) -> None:
        """Update datastore schema to include embedding field.

        Args:
            project_id: Google Cloud project ID
            location: Google Cloud location
            data_store_id: Target datastore ID
            embedding_column: Name of embedding column
            client_options: Client options for API
        """
        schema_client = discoveryengine.SchemaServiceClient(
            client_options=client_options
        )
        collection = "default_collection"

        name = f"projects/{project_id}/locations/{location}/collections/{collection}/dataStores/{data_store_id}/schemas/default_schema"

        schema = schema_client.get_schema(
            request=discoveryengine.GetSchemaRequest(name=name)
        )
        new_schema_json = update_schema_as_json(
            original_schema=schema.json_schema,
            embedding_dimension=embedding_dimension,
            field_name=field_name,
        )
        new_schema = discoveryengine.Schema(json_schema=new_schema_json, name=name)

        operation = schema_client.update_schema(
            request=discoveryengine.UpdateSchemaRequest(
                schema=new_schema, allow_missing=True
            ),
            timeout=1800,
        )
        logging.info(f"Waiting for schema update operation: {operation.operation.name}")
        operation.result()

    def add_data_in_store(
        project_id: str,
        location: str,
        data_store_id: str,
        input_files_uri: str,
        client_options: ClientOptions | None = None,
    ) -> None:
        """Import documents into datastore.

        Args:
            project_id: Google Cloud project ID
            location: Google Cloud location
            data_store_id: Target datastore ID
            input_files_uri: URI of input files
            client_options: Client options for API
        """
        client = discoveryengine.DocumentServiceClient(client_options=client_options)

        parent = client.branch_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            branch="default_branch",
        )

        request = discoveryengine.ImportDocumentsRequest(
            parent=parent,
            gcs_source=discoveryengine.GcsSource(
                input_uris=[input_files_uri],
                data_schema="document",
            ),
            reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL,
        )

        operation = client.import_documents(request=request)
        logging.info(f"Waiting for import operation: {operation.operation.name}")
        operation.result()

    client_options = ClientOptions(
        api_endpoint=f"{data_store_region}-discoveryengine.googleapis.com"
    )

    logging.info("Updating data store schema...")
    update_data_store_schema(
        project_id=project_id,
        location=data_store_region,
        data_store_id=data_store_id,
        field_name=embedding_column,
        client_options=client_options,
    )
    logging.info("Schema updated successfully")

    logging.info("Importing data into store...")
    add_data_in_store(
        project_id=project_id,
        location=data_store_region,
        data_store_id=data_store_id,
        client_options=client_options,
        input_files_uri=input_files.uri,
    )
    logging.info("Data import completed")
    logging.info(
        "Sleeping for 3 minutes to allow Vertex AI Search to properly index the data..."
    )
    time.sleep(180)  # Sleep for 180 seconds (3 minutes)
    logging.info("Sleep completed. Data indexing should now be complete.")
