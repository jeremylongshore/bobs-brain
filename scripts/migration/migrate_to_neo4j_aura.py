#!/usr/bin/env python3
"""
Neo4j Aura Migration Script
Migrates from self-hosted Neo4j VM to Neo4j Aura Free
"""

import json
import logging
import os
import time

from google.cloud import secretmanager
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Neo4jAuraMigration:
    def __init__(self):
        self.project_id = "bobs-house-ai"

        # Current VM Neo4j credentials
        self.vm_uri = "bolt://10.128.0.2:7687"
        self.vm_user = "neo4j"
        self.vm_password = "BobBrain2025"

        # Neo4j Aura credentials (to be filled after creation)
        # Neo4j Aura Free provides these after sign-up:
        # - Connection URI: neo4j+s://xxxxx.databases.neo4j.io
        # - Username: neo4j (default)
        # - Password: (generated)

        # For now, we'll use environment variables for Aura credentials
        self.aura_uri = os.environ.get("NEO4J_AURA_URI", "")
        self.aura_user = os.environ.get("NEO4J_AURA_USER", "neo4j")
        self.aura_password = os.environ.get("NEO4J_AURA_PASSWORD", "")

    def test_vm_connection(self):
        """Test connection to current VM Neo4j"""
        try:
            driver = GraphDatabase.driver(self.vm_uri, auth=(self.vm_user, self.vm_password))
            with driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                logger.info(f"✅ VM Neo4j connected. Node count: {count}")
                driver.close()
                return True
        except Exception as e:
            logger.error(f"❌ VM Neo4j connection failed: {e}")
            return False

    def test_aura_connection(self):
        """Test connection to Neo4j Aura"""
        if not self.aura_uri or not self.aura_password:
            logger.warning("⚠️ Neo4j Aura credentials not set")
            logger.info(
                """
To set up Neo4j Aura Free:
1. Go to: https://console.neo4j.io
2. Sign up for Neo4j AuraDB Free
3. Create a new database (select Free tier)
4. Save the connection details:
   - Connection URI (neo4j+s://...)
   - Password (auto-generated)
5. Set environment variables:
   export NEO4J_AURA_URI="neo4j+s://xxxxx.databases.neo4j.io"
   export NEO4J_AURA_PASSWORD="your-generated-password"
            """
            )
            return False

        try:
            driver = GraphDatabase.driver(self.aura_uri, auth=(self.aura_user, self.aura_password))
            with driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                logger.info(f"✅ Neo4j Aura connected. Node count: {count}")
                driver.close()
                return True
        except Exception as e:
            logger.error(f"❌ Neo4j Aura connection failed: {e}")
            return False

    def export_vm_data(self):
        """Export data from VM Neo4j"""
        logger.info("Exporting data from VM Neo4j...")

        try:
            driver = GraphDatabase.driver(self.vm_uri, auth=(self.vm_user, self.vm_password))

            nodes = []
            relationships = []

            with driver.session() as session:
                # Export all nodes
                result = session.run(
                    """
                    MATCH (n)
                    RETURN n, labels(n) as labels, properties(n) as props
                """
                )
                for record in result:
                    nodes.append({"labels": record["labels"], "properties": dict(record["props"])})

                # Export all relationships
                result = session.run(
                    """
                    MATCH (a)-[r]->(b)
                    RETURN id(a) as start_id, id(b) as end_id,
                           type(r) as type, properties(r) as props,
                           labels(a) as start_labels, labels(b) as end_labels,
                           properties(a) as start_props, properties(b) as end_props
                """
                )
                for record in result:
                    relationships.append(
                        {
                            "start": {"labels": record["start_labels"], "properties": dict(record["start_props"])},
                            "end": {"labels": record["end_labels"], "properties": dict(record["end_props"])},
                            "type": record["type"],
                            "properties": dict(record["props"]) if record["props"] else {},
                        }
                    )

            driver.close()

            logger.info(f"✅ Exported {len(nodes)} nodes and {len(relationships)} relationships")

            # Save to file as backup
            with open("neo4j_backup.json", "w") as f:
                json.dump(
                    {"nodes": nodes, "relationships": relationships, "export_timestamp": time.time()},
                    f,
                    indent=2,
                    default=str,
                )

            return nodes, relationships

        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return None, None

    def import_to_aura(self, nodes, relationships):
        """Import data to Neo4j Aura"""
        if not self.aura_uri or not self.aura_password:
            logger.error("❌ Neo4j Aura credentials not set")
            return False

        logger.info("Importing data to Neo4j Aura...")

        try:
            driver = GraphDatabase.driver(self.aura_uri, auth=(self.aura_user, self.aura_password))

            with driver.session() as session:
                # Clear existing data (careful in production!)
                session.run("MATCH (n) DETACH DELETE n")

                # Import nodes
                node_map = {}
                for i, node in enumerate(nodes):
                    labels = ":".join(node["labels"]) if node["labels"] else "Node"
                    props = node["properties"]

                    # Create unique identifier for node mapping
                    node_id = f"node_{i}"
                    props["_import_id"] = node_id

                    # Build properties string
                    props_str = ", ".join([f"{k}: ${k}" for k in props.keys()])

                    query = f"CREATE (n:{labels} {{{props_str}}}) RETURN n"
                    session.run(query, **props)

                    node_map[json.dumps(props, sort_keys=True)] = node_id

                logger.info(f"✅ Imported {len(nodes)} nodes")

                # Import relationships
                for rel in relationships:
                    start_key = json.dumps(rel["start"]["properties"], sort_keys=True)
                    end_key = json.dumps(rel["end"]["properties"], sort_keys=True)

                    if start_key in node_map and end_key in node_map:
                        start_id = node_map[start_key]
                        end_id = node_map[end_key]

                        rel_type = rel["type"]
                        rel_props = rel["properties"]

                        if rel_props:
                            props_str = ", ".join([f"{k}: ${k}" for k in rel_props.keys()])
                            query = f"""
                                MATCH (a {{_import_id: $start_id}})
                                MATCH (b {{_import_id: $end_id}})
                                CREATE (a)-[r:{rel_type} {{{props_str}}}]->(b)
                                RETURN r
                            """
                            session.run(query, start_id=start_id, end_id=end_id, **rel_props)
                        else:
                            query = f"""
                                MATCH (a {{_import_id: $start_id}})
                                MATCH (b {{_import_id: $end_id}})
                                CREATE (a)-[r:{rel_type}]->(b)
                                RETURN r
                            """
                            session.run(query, start_id=start_id, end_id=end_id)

                # Clean up import IDs
                session.run("MATCH (n) REMOVE n._import_id")

                logger.info(f"✅ Imported {len(relationships)} relationships")

            driver.close()
            return True

        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return False

    def save_credentials_to_secret_manager(self):
        """Save Neo4j Aura credentials to Google Secret Manager"""
        if not self.aura_uri or not self.aura_password:
            logger.warning("⚠️ Neo4j Aura credentials not set, skipping Secret Manager")
            return False

        try:
            client = secretmanager.SecretManagerServiceClient()
            parent = f"projects/{self.project_id}"

            secrets = {
                "neo4j-aura-uri": self.aura_uri,
                "neo4j-aura-password": self.aura_password,
                "neo4j-aura-user": self.aura_user,
            }

            for secret_id, secret_value in secrets.items():
                # Try to create the secret
                try:
                    secret = client.create_secret(
                        request={"parent": parent, "secret_id": secret_id, "secret": {"replication": {"automatic": {}}}}
                    )
                    logger.info(f"✅ Created secret: {secret_id}")
                except:
                    # Secret might already exist
                    pass

                # Add secret version
                secret_name = f"{parent}/secrets/{secret_id}"
                response = client.add_secret_version(
                    request={"parent": secret_name, "payload": {"data": secret_value.encode("UTF-8")}}
                )
                logger.info(f"✅ Added secret version for: {secret_id}")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to save to Secret Manager: {e}")
            return False

    def migrate(self):
        """Execute full migration"""
        logger.info("=" * 60)
        logger.info("🚀 Starting Neo4j VM to Aura migration")
        logger.info("=" * 60)

        # Step 1: Test VM connection
        if not self.test_vm_connection():
            logger.error("Cannot connect to VM Neo4j. Is it running?")
            return False

        # Step 2: Test Aura connection
        if not self.test_aura_connection():
            logger.error("Cannot connect to Neo4j Aura. Please set up credentials.")
            return False

        # Step 3: Export data from VM
        nodes, relationships = self.export_vm_data()
        if nodes is None:
            logger.error("Failed to export data from VM")
            return False

        # Step 4: Import data to Aura
        if not self.import_to_aura(nodes, relationships):
            logger.error("Failed to import data to Aura")
            return False

        # Step 5: Save credentials to Secret Manager
        self.save_credentials_to_secret_manager()

        logger.info("=" * 60)
        logger.info("✅ Migration completed successfully!")
        logger.info("=" * 60)

        return True


if __name__ == "__main__":
    migrator = Neo4jAuraMigration()

    # Check if Aura credentials are set
    if not migrator.aura_uri:
        print(
            """
Neo4j Aura Free Setup Instructions:
====================================
1. Go to: https://console.neo4j.io
2. Click "Start Free"
3. Create a new AuraDB Free instance
4. Save your credentials and run:

export NEO4J_AURA_URI="neo4j+s://xxxxx.databases.neo4j.io"
export NEO4J_AURA_PASSWORD="your-generated-password"
python3 migrate_to_neo4j_aura.py
        """
        )
    else:
        # Run migration
        if migrator.migrate():
            print(
                """
✅ Migration complete!

Next steps:
1. Update Bob Brain environment variables
2. Deploy Bob with new Neo4j Aura credentials
3. Test Graphiti integration
4. Stop the VM: gcloud compute instances stop bob-neo4j --zone=us-central1-a
5. Delete the VM: gcloud compute instances delete bob-neo4j --zone=us-central1-a
            """
            )
        else:
            print("❌ Migration failed. Check logs above.")
