#!/usr/bin/env python3
"""
Setup Official Graphiti Framework with Neo4j Aura
Uses the open-source Graphiti from https://github.com/getzep/graphiti
Configured to work without OpenAI using local embeddings
"""

import logging
import os
import subprocess
import sys
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphitiCloudSetup:
    """Setup Graphiti framework on Google Cloud with Neo4j Aura"""

    def __init__(self):
        self.project_id = "bobs-house-ai"

    def install_graphiti(self):
        """Install the official Graphiti framework from GitHub"""
        logger.info("Installing official Graphiti framework...")

        try:
            # Install latest Graphiti
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "graphiti-core"], check=True)

            # Install sentence-transformers for local embeddings (no OpenAI needed)
            subprocess.run([sys.executable, "-m", "pip", "install", "sentence-transformers", "torch"], check=True)

            logger.info("✅ Graphiti and dependencies installed")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Installation failed: {e}")
            return False

    def setup_neo4j_aura(self):
        """Instructions for setting up Neo4j Aura Free"""

        instructions = """
        ========================================
        NEO4J AURA FREE SETUP INSTRUCTIONS
        ========================================

        1. Go to: https://console.neo4j.io
        2. Click "Start Free" or "Sign Up"
        3. Select "AuraDB Free" (not AuraDS)
        4. Create your instance:
           - Choose region closest to us-central1
           - Instance will be created with:
             * 1 GB storage
             * 200K nodes limit
             * 400K relationships limit

        5. SAVE YOUR CREDENTIALS:
           - Connection URI: neo4j+s://xxxxx.databases.neo4j.io
           - Username: neo4j (default)
           - Password: (auto-generated, save it!)

        6. Set environment variables:
           export NEO4J_AURA_URI="neo4j+s://xxxxx.databases.neo4j.io"
           export NEO4J_AURA_USER="neo4j"
           export NEO4J_AURA_PASSWORD="your-password-here"

        7. Instance features:
           - Auto-pauses after 3 days of inactivity
           - Can be resumed anytime
           - Free forever (with limits)

        ========================================
        """

        print(instructions)

        # Check if credentials are set
        aura_uri = os.environ.get("NEO4J_AURA_URI")
        aura_password = os.environ.get("NEO4J_AURA_PASSWORD")

        if aura_uri and aura_password:
            logger.info("✅ Neo4j Aura credentials detected")
            return True
        else:
            logger.warning("⚠️ Neo4j Aura credentials not set")
            return False

    def create_graphiti_config(self):
        """Create Graphiti configuration without OpenAI"""

        config_content = '''
"""
Graphiti Configuration for Bob's Brain
Uses local embeddings instead of OpenAI
"""

import os
from graphiti_core import Graphiti
from graphiti_core.llm_client.client import LLMClient
from graphiti_core.embedder.client import EmbedderClient

class LocalEmbedder(EmbedderClient):
    """Local embedder using sentence-transformers (no OpenAI needed)"""

    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    async def embed(self, text: str):
        """Generate embeddings locally"""
        return self.model.encode(text).tolist()

    async def embed_batch(self, texts: list):
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts).tolist()

class NoOpLLM(LLMClient):
    """No-op LLM client (Graphiti without AI generation)"""

    async def generate(self, prompt: str):
        """Return empty response - we don't need AI generation"""
        return ""

    async def extract_entities(self, text: str):
        """Simple entity extraction without AI"""
        import re

        entities = []

        # Extract equipment mentions
        equipment_patterns = [
            r'\b(excavator|skid steer|loader|dozer|grader|tractor|mower)\b',
            r'\b(bobcat|caterpillar|john deere|kubota|case)\b'
        ]

        for pattern in equipment_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                entities.append({
                    "name": match.title(),
                    "type": "Equipment"
                })

        # Extract error codes
        error_pattern = r'\b[A-Z]{1,4}[-]?\d{3,5}\b'
        errors = re.findall(error_pattern, text)
        for error in errors:
            entities.append({
                "name": error,
                "type": "ErrorCode"
            })

        return entities

def create_graphiti_instance():
    """Create Graphiti instance with local processing"""

    # Get Neo4j Aura credentials
    neo4j_uri = os.environ.get("NEO4J_AURA_URI") or os.environ.get("NEO4J_URI")
    neo4j_user = os.environ.get("NEO4J_AURA_USER", "neo4j")
    neo4j_password = os.environ.get("NEO4J_AURA_PASSWORD") or os.environ.get("NEO4J_PASSWORD")

    if not neo4j_uri or not neo4j_password:
        raise ValueError("Neo4j credentials not set")

    # Create Graphiti with local embedder and no-op LLM
    graphiti = Graphiti(
        uri=neo4j_uri,
        user=neo4j_user,
        password=neo4j_password,
        embedder=LocalEmbedder(),
        llm_client=NoOpLLM()
    )

    return graphiti

# Export for use in Bob Brain
__all__ = ['create_graphiti_instance', 'LocalEmbedder', 'NoOpLLM']
'''

        # Save configuration
        config_path = "/home/jeremylongshore/bobs-brain/src/graphiti_config.py"
        with open(config_path, "w") as f:
            f.write(config_content)

        logger.info(f"✅ Graphiti configuration saved to {config_path}")
        return True

    def create_deployment_script(self):
        """Create script to deploy Graphiti on Cloud Run"""

        script_content = """#!/bin/bash
# Deploy Graphiti-enabled Bob Brain to Cloud Run

echo "Deploying Bob Brain with Graphiti to Cloud Run..."

# Build and deploy
gcloud run deploy bobs-brain \\
    --source . \\
    --region us-central1 \\
    --min-instances 1 \\
    --max-instances 10 \\
    --memory 2Gi \\
    --timeout 3600 \\
    --set-env-vars "NEO4J_AURA_URI=${NEO4J_AURA_URI},NEO4J_AURA_USER=${NEO4J_AURA_USER},NEO4J_AURA_PASSWORD=${NEO4J_AURA_PASSWORD},PROJECT_ID=bobs-house-ai" \\
    --vpc-connector bob-vpc-connector \\
    --vpc-egress private-ranges-only

echo "✅ Deployment complete!"
echo "Test at: https://bobs-brain-sytrh5wz5q-uc.a.run.app/health"
"""

        script_path = "/home/jeremylongshore/bobs-brain/deploy_graphiti.sh"
        with open(script_path, "w") as f:
            f.write(script_content)

        os.chmod(script_path, 0o755)
        logger.info(f"✅ Deployment script saved to {script_path}")
        return True

    def setup_circle_of_life_integration(self):
        """Create integration between Graphiti and Circle of Life (BigQuery)"""

        integration_content = '''
"""
Circle of Life Integration with Graphiti
Syncs knowledge graph patterns to BigQuery for learning
"""

import logging
from google.cloud import bigquery
from datetime import datetime

logger = logging.getLogger(__name__)

class CircleOfLifeGraphiti:
    """Integrates Graphiti knowledge graph with Circle of Life learning system"""

    def __init__(self, graphiti_instance, project_id="bobs-house-ai"):
        self.graphiti = graphiti_instance
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)

        # Ensure BigQuery tables exist
        self._ensure_tables()

    def _ensure_tables(self):
        """Create BigQuery tables for Circle of Life if they don't exist"""

        dataset_id = f"{self.project_id}.circle_of_life"

        # Create dataset
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        self.bq_client.create_dataset(dataset, exists_ok=True)

        # Create learning patterns table
        table_id = f"{dataset_id}.graphiti_patterns"
        schema = [
            bigquery.SchemaField("pattern_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("pattern_type", "STRING"),
            bigquery.SchemaField("pattern_value", "JSON"),
            bigquery.SchemaField("frequency", "INTEGER"),
            bigquery.SchemaField("confidence", "FLOAT"),
            bigquery.SchemaField("extracted_at", "TIMESTAMP"),
            bigquery.SchemaField("source", "STRING"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)

        logger.info(f"✅ Circle of Life tables ready in BigQuery")

    async def sync_patterns(self):
        """Sync patterns from Graphiti to BigQuery for learning"""

        try:
            # Query Graphiti for patterns
            patterns = await self.graphiti.get_patterns()

            # Transform and store in BigQuery
            rows = []
            for pattern in patterns:
                rows.append({
                    "pattern_id": pattern.get("id"),
                    "pattern_type": pattern.get("type"),
                    "pattern_value": pattern.get("value"),
                    "frequency": pattern.get("frequency", 1),
                    "confidence": pattern.get("confidence", 0.5),
                    "extracted_at": datetime.now(),
                    "source": "graphiti"
                })

            if rows:
                table_id = f"{self.project_id}.circle_of_life.graphiti_patterns"
                errors = self.bq_client.insert_rows_json(table_id, rows)

                if errors:
                    logger.error(f"BigQuery errors: {errors}")
                else:
                    logger.info(f"✅ Synced {len(rows)} patterns to Circle of Life")

            return len(rows)

        except Exception as e:
            logger.error(f"Pattern sync failed: {e}")
            return 0

    async def learn_from_feedback(self, feedback: dict):
        """Process feedback and update knowledge graph"""

        try:
            # Add feedback as episode in Graphiti
            episode_id = await self.graphiti.add_episode(
                content=feedback.get("content", ""),
                metadata={
                    "type": "feedback",
                    "user": feedback.get("user", "system"),
                    "timestamp": datetime.now().isoformat()
                }
            )

            # Sync to BigQuery
            await self.sync_patterns()

            logger.info(f"✅ Learned from feedback: {episode_id}")
            return episode_id

        except Exception as e:
            logger.error(f"Learning failed: {e}")
            return None

# Export for use
__all__ = ['CircleOfLifeGraphiti']
'''

        integration_path = "/home/jeremylongshore/bobs-brain/src/circle_of_life_graphiti.py"
        with open(integration_path, "w") as f:
            f.write(integration_content)

        logger.info(f"✅ Circle of Life integration saved to {integration_path}")
        return True

    def run_setup(self):
        """Run complete setup process"""

        logger.info("=" * 60)
        logger.info("🚀 GRAPHITI CLOUD SETUP")
        logger.info("=" * 60)

        # Step 1: Install Graphiti
        if not self.install_graphiti():
            logger.error("Failed to install Graphiti")
            return False

        # Step 2: Setup Neo4j Aura
        if not self.setup_neo4j_aura():
            logger.warning("Neo4j Aura setup incomplete - follow instructions above")

        # Step 3: Create configuration
        if not self.create_graphiti_config():
            logger.error("Failed to create configuration")
            return False

        # Step 4: Create deployment script
        if not self.create_deployment_script():
            logger.error("Failed to create deployment script")
            return False

        # Step 5: Setup Circle of Life integration
        if not self.setup_circle_of_life_integration():
            logger.error("Failed to create Circle of Life integration")
            return False

        logger.info("=" * 60)
        logger.info("✅ GRAPHITI CLOUD SETUP COMPLETE")
        logger.info("=" * 60)

        print(
            """
Next Steps:
===========
1. Set up Neo4j Aura Free (if not done):
   - Go to https://console.neo4j.io
   - Create free instance
   - Set environment variables

2. Migrate data (if needed):
   python3 migrate_to_neo4j_aura.py

3. Deploy to Cloud Run:
   ./deploy_graphiti.sh

4. Test the system:
   curl https://bobs-brain-sytrh5wz5q-uc.a.run.app/health

5. Stop the old VM (save $50/month):
   gcloud compute instances delete bob-neo4j --zone=us-central1-a
        """
        )

        return True


if __name__ == "__main__":
    setup = GraphitiCloudSetup()
    setup.run_setup()
