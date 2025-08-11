#!/usr/bin/env python3
"""
Official Google Cloud Vertex AI AutoML Setup
Based on latest Google Cloud documentation (2024/2025)
"""

# OFFICIAL INSTALLATION REQUIREMENTS:
# pip install --upgrade google-cloud-aiplatform==1.38.0
# pip install --upgrade google-cloud-bigquery==3.11.4
# pip install --upgrade google-cloud-storage==2.10.0

import os
from typing import List, Dict, Optional
from google.cloud import aiplatform
from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexAIAutoMLOfficial:
    """
    Official implementation following Google Cloud Vertex AI documentation
    AutoML Version: Vertex AI AutoML (not AutoML Tables which is deprecated)
    """
    
    def __init__(self, project_id: str, location: str = 'us-central1'):
        """
        Initialize Vertex AI following official documentation
        https://cloud.google.com/vertex-ai/docs/start/install-sdk
        """
        
        # Official initialization method
        aiplatform.init(
            project=project_id,
            location=location,
            staging_bucket=f'gs://{project_id}-vertex-staging'  # Optional but recommended
        )
        
        self.project_id = project_id
        self.location = location
        logger.info(f"✅ Vertex AI initialized: {project_id} in {location}")
    
    def create_tabular_dataset_from_bigquery(
        self,
        display_name: str,
        bigquery_source: str
    ) -> aiplatform.TabularDataset:
        """
        Create dataset from BigQuery following official docs
        https://cloud.google.com/vertex-ai/docs/datasets/create-dataset-api
        
        Args:
            display_name: Name for the dataset
            bigquery_source: Format: 'bq://project.dataset.table'
        """
        
        dataset = aiplatform.TabularDataset.create(
            display_name=display_name,
            bq_source=bigquery_source,
        )
        
        logger.info(f"✅ Dataset created: {dataset.resource_name}")
        return dataset
    
    def create_tabular_dataset_from_gcs(
        self,
        display_name: str,
        gcs_source: List[str]
    ) -> aiplatform.TabularDataset:
        """
        Create dataset from Cloud Storage CSV
        
        Args:
            display_name: Name for the dataset
            gcs_source: List of GCS paths ['gs://bucket/file.csv']
        """
        
        dataset = aiplatform.TabularDataset.create(
            display_name=display_name,
            gcs_source=gcs_source,
        )
        
        logger.info(f"✅ Dataset created: {dataset.resource_name}")
        return dataset
    
    def train_automl_tabular_regression(
        self,
        dataset: aiplatform.TabularDataset,
        target_column: str,
        display_name: str,
        budget_hours: float = 1.0,
        column_transformations: Optional[List[Dict]] = None
    ) -> aiplatform.Model:
        """
        Train AutoML regression model following official documentation
        https://cloud.google.com/vertex-ai/docs/tabular-data/classification-regression/train-model
        
        Args:
            dataset: TabularDataset object
            target_column: Name of the target column
            display_name: Name for the training job
            budget_hours: Training budget in node hours (1 hour = ~$20)
            column_transformations: Optional column transformations
        """
        
        # Create training job
        job = aiplatform.AutoMLTabularTrainingJob(
            display_name=display_name,
            optimization_prediction_type="regression",
            optimization_objective="minimize-rmse",  # For regression
            column_transformations=column_transformations or [{"auto": {}}],
        )
        
        # Run training
        model = job.run(
            dataset=dataset,
            target_column=target_column,
            training_fraction_split=0.8,
            validation_fraction_split=0.1,
            test_fraction_split=0.1,
            budget_milli_node_hours=int(budget_hours * 1000),
            model_display_name=f"{display_name}_model",
            disable_early_stopping=False,
        )
        
        logger.info(f"✅ Model trained: {model.resource_name}")
        return model
    
    def train_automl_tabular_classification(
        self,
        dataset: aiplatform.TabularDataset,
        target_column: str,
        display_name: str,
        budget_hours: float = 1.0
    ) -> aiplatform.Model:
        """
        Train AutoML classification model
        
        Args:
            dataset: TabularDataset object
            target_column: Name of the target column
            display_name: Name for the training job
            budget_hours: Training budget in node hours
        """
        
        job = aiplatform.AutoMLTabularTrainingJob(
            display_name=display_name,
            optimization_prediction_type="classification",
            optimization_objective="maximize-au-roc",  # For binary classification
            # Use "maximize-recall-at-precision" or "maximize-precision-at-recall" for specific needs
        )
        
        model = job.run(
            dataset=dataset,
            target_column=target_column,
            training_fraction_split=0.8,
            validation_fraction_split=0.1,
            test_fraction_split=0.1,
            budget_milli_node_hours=int(budget_hours * 1000),
            model_display_name=f"{display_name}_model",
        )
        
        logger.info(f"✅ Model trained: {model.resource_name}")
        return model
    
    def train_automl_tabular_forecasting(
        self,
        dataset: aiplatform.TabularDataset,
        target_column: str,
        time_column: str,
        time_series_identifier_column: str,
        display_name: str,
        budget_hours: float = 1.0,
        forecast_horizon: int = 30
    ) -> aiplatform.Model:
        """
        Train AutoML forecasting model
        
        Args:
            dataset: TabularDataset object
            target_column: Column to forecast
            time_column: Timestamp column
            time_series_identifier_column: Column that identifies time series
            display_name: Name for the training job
            budget_hours: Training budget
            forecast_horizon: Number of time points to forecast
        """
        
        job = aiplatform.AutoMLForecastingTrainingJob(
            display_name=display_name,
            optimization_objective="minimize-rmse",
            column_transformations=[{"auto": {}}],
        )
        
        model = job.run(
            dataset=dataset,
            target_column=target_column,
            time_column=time_column,
            time_series_identifier_column=time_series_identifier_column,
            available_at_forecast_columns=[],
            unavailable_at_forecast_columns=[],
            forecast_horizon=forecast_horizon,
            data_granularity_unit="day",
            data_granularity_count=1,
            training_fraction_split=0.8,
            validation_fraction_split=0.1,
            test_fraction_split=0.1,
            budget_milli_node_hours=int(budget_hours * 1000),
            model_display_name=f"{display_name}_model",
        )
        
        logger.info(f"✅ Forecasting model trained: {model.resource_name}")
        return model
    
    def deploy_model(
        self,
        model: aiplatform.Model,
        endpoint_display_name: str,
        machine_type: str = "n1-standard-4",
        min_replicas: int = 1,
        max_replicas: int = 3
    ) -> aiplatform.Endpoint:
        """
        Deploy model to endpoint following official documentation
        https://cloud.google.com/vertex-ai/docs/predictions/deploy-model-api
        
        Args:
            model: Trained model
            endpoint_display_name: Name for the endpoint
            machine_type: Machine type for serving
            min_replicas: Minimum number of replicas
            max_replicas: Maximum number of replicas
        """
        
        # Create endpoint
        endpoint = aiplatform.Endpoint.create(
            display_name=endpoint_display_name,
        )
        
        # Deploy model to endpoint
        model.deploy(
            endpoint=endpoint,
            deployed_model_display_name=f"{endpoint_display_name}_deployed",
            machine_type=machine_type,
            min_replica_count=min_replicas,
            max_replica_count=max_replicas,
            accelerator_type=None,  # No GPU needed for tabular
            accelerator_count=0,
        )
        
        logger.info(f"✅ Model deployed to: {endpoint.resource_name}")
        return endpoint
    
    def batch_predict(
        self,
        model: aiplatform.Model,
        input_source: str,
        output_uri: str,
        machine_type: str = "n1-standard-4"
    ) -> aiplatform.BatchPredictionJob:
        """
        Run batch prediction
        
        Args:
            model: Trained model
            input_source: BigQuery table or GCS file
            output_uri: GCS path for output
            machine_type: Machine type for prediction
        """
        
        batch_prediction_job = model.batch_predict(
            job_display_name="batch_prediction",
            instances_format="bigquery" if input_source.startswith("bq://") else "csv",
            bigquery_source=input_source if input_source.startswith("bq://") else None,
            gcs_source=input_source if input_source.startswith("gs://") else None,
            predictions_format="bigquery" if input_source.startswith("bq://") else "csv",
            bigquery_destination_prefix=output_uri if input_source.startswith("bq://") else None,
            gcs_destination_prefix=output_uri if input_source.startswith("gs://") else None,
            machine_type=machine_type,
            starting_replica_count=1,
            max_replica_count=3,
        )
        
        logger.info(f"✅ Batch prediction started: {batch_prediction_job.resource_name}")
        return batch_prediction_job
    
    def online_predict(
        self,
        endpoint: aiplatform.Endpoint,
        instances: List[Dict]
    ) -> List:
        """
        Make online predictions
        
        Args:
            endpoint: Deployed endpoint
            instances: List of instances to predict
        """
        
        predictions = endpoint.predict(instances=instances)
        return predictions.predictions


def main():
    """Example usage following official Google Cloud patterns"""
    
    # Initialize
    automl = VertexAIAutoMLOfficial(
        project_id="bobs-house-ai",
        location="us-central1"
    )
    
    # Create dataset from BigQuery
    dataset = automl.create_tabular_dataset_from_bigquery(
        display_name="repair_quotes_dataset",
        bigquery_source="bq://bobs-house-ai.scraped_data.repair_quotes"
    )
    
    # Train regression model for price prediction
    model = automl.train_automl_tabular_regression(
        dataset=dataset,
        target_column="quoted_price",
        display_name="repair_price_predictor",
        budget_hours=1.0,  # $20 worth of training
        column_transformations=[
            {"numeric": {"column_name": "vehicle_year"}},
            {"categorical": {"column_name": "vehicle_make"}},
            {"categorical": {"column_name": "vehicle_model"}},
            {"categorical": {"column_name": "repair_type"}},
            {"categorical": {"column_name": "shop_name"}},
            {"numeric": {"column_name": "parts_cost"}},
            {"numeric": {"column_name": "labor_cost"}},
        ]
    )
    
    # Deploy model
    endpoint = automl.deploy_model(
        model=model,
        endpoint_display_name="repair_price_endpoint",
        machine_type="n1-standard-4",
        min_replicas=1,
        max_replicas=2
    )
    
    # Make prediction
    prediction = automl.online_predict(
        endpoint=endpoint,
        instances=[
            {
                "vehicle_year": 2020,
                "vehicle_make": "Toyota",
                "vehicle_model": "Camry",
                "repair_type": "brake_replacement",
                "shop_name": "AutoShop",
                "parts_cost": 500.0,
                "labor_cost": 300.0
            }
        ]
    )
    
    print(f"Predicted price: ${prediction[0]}")
    
    # COSTS WITH YOUR CREDITS:
    # - Dataset creation: Free
    # - Training (1 hour): ~$20
    # - Deployment: ~$50/month for endpoint
    # - Predictions: ~$0.001 per 1000 predictions
    # Total: Well within your $2,251 credits!

if __name__ == "__main__":
    main()