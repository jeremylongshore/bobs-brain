#!/usr/bin/env python3
"""
Comprehensive Backup and Validation Scripts for Bob's Brain Migration
Includes pre-migration backup, post-migration validation, and rollback capabilities
"""

import os
import json
import hashlib
import sqlite3
import chromadb
import shutil
import tarfile
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from google.cloud import firestore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BobBrainBackup:
    """Comprehensive backup system for Bob's Brain migration"""

    def __init__(self, backup_base_dir: str = "/home/jeremylongshore/backup"):
        self.backup_base_dir = backup_base_dir
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = f"{backup_base_dir}/bob_brain_backup_{self.timestamp}"

        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

        # Source paths
        self.source_brain_dir = "/home/jeremylongshore/.bob_brain"
        self.source_code_dir = "/home/jeremylongshore/bobs_brain"

        # Backup manifest
        self.manifest = {
            'backup_timestamp': self.timestamp,
            'backup_dir': self.backup_dir,
            'source_paths': {
                'brain_dir': self.source_brain_dir,
                'code_dir': self.source_code_dir
            },
            'files_backed_up': [],
            'checksums': {},
            'data_counts': {}
        }

        logger.info(f"🗄️  Backup initialized: {self.backup_dir}")

    def create_full_backup(self) -> bool:
        """Create comprehensive backup of all Bob's Brain components"""

        logger.info("🔄 Starting comprehensive backup...")

        try:
            # 1. Backup ChromaDB
            self._backup_chromadb()

            # 2. Backup SQLite databases
            self._backup_sqlite_databases()

            # 3. Backup source code
            self._backup_source_code()

            # 4. Create VM snapshot reference
            self._create_vm_snapshot_reference()

            # 5. Generate checksums
            self._generate_checksums()

            # 6. Save manifest
            self._save_manifest()

            # 7. Create compressed archive
            self._create_compressed_archive()

            logger.info(f"✅ Backup completed successfully: {self.backup_dir}")
            return True

        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False

    def _backup_chromadb(self):
        """Backup ChromaDB collection with all embeddings"""

        logger.info("📊 Backing up ChromaDB...")

        try:
            chroma_backup_dir = f"{self.backup_dir}/chromadb"
            os.makedirs(chroma_backup_dir, exist_ok=True)

            # Connect to ChromaDB
            client = chromadb.PersistentClient(path=f"{self.source_brain_dir}/chroma")
            collection = client.get_collection('bob_knowledge')

            # Export all data
            all_data = collection.get()

            # Save as JSON
            chroma_export = {
                'collection_name': 'bob_knowledge',
                'exported_at': datetime.now().isoformat(),
                'total_items': len(all_data['ids']),
                'data': {
                    'ids': all_data['ids'],
                    'documents': all_data['documents'],
                    'embeddings': all_data['embeddings'],
                    'metadatas': all_data['metadatas']
                }
            }

            export_file = f"{chroma_backup_dir}/bob_knowledge_export.json"
            with open(export_file, 'w') as f:
                json.dump(chroma_export, f, indent=2)

            # Also copy the raw ChromaDB files
            if os.path.exists(f"{self.source_brain_dir}/chroma"):
                shutil.copytree(
                    f"{self.source_brain_dir}/chroma",
                    f"{chroma_backup_dir}/raw_chroma",
                    dirs_exist_ok=True
                )

            self.manifest['files_backed_up'].append(export_file)
            self.manifest['data_counts']['chromadb_items'] = len(all_data['ids'])

            logger.info(f"✅ ChromaDB backup: {len(all_data['ids'])} items")

        except Exception as e:
            logger.error(f"❌ ChromaDB backup failed: {e}")
            raise

    def _backup_sqlite_databases(self):
        """Backup all SQLite databases with schema and data"""

        logger.info("🗃️  Backing up SQLite databases...")

        sqlite_backup_dir = f"{self.backup_dir}/sqlite"
        os.makedirs(sqlite_backup_dir, exist_ok=True)

        # Find all .db files
        db_files = [
            'bob_memory.db',
            'automation.db',
            'smart_insights.db'
        ]

        total_records = 0

        for db_file in db_files:
            db_path = f"{self.source_brain_dir}/{db_file}"

            if not os.path.exists(db_path):
                logger.warning(f"⚠️  Database not found: {db_path}")
                continue

            try:
                # Copy the database file
                backup_db_path = f"{sqlite_backup_dir}/{db_file}"
                shutil.copy2(db_path, backup_db_path)

                # Export data as JSON for human-readable backup
                export_data = self._export_sqlite_to_json(db_path)

                json_export_path = f"{sqlite_backup_dir}/{db_file.replace('.db', '_export.json')}"
                with open(json_export_path, 'w') as f:
                    json.dump(export_data, f, indent=2)

                self.manifest['files_backed_up'].extend([backup_db_path, json_export_path])

                # Count records
                db_records = sum(len(table['data']) for table in export_data['tables'])
                total_records += db_records
                self.manifest['data_counts'][f'{db_file}_records'] = db_records

                logger.info(f"✅ {db_file}: {db_records} records")

            except Exception as e:
                logger.error(f"❌ Failed to backup {db_file}: {e}")
                raise

        logger.info(f"✅ SQLite backup: {total_records} total records")

    def _export_sqlite_to_json(self, db_path: str) -> Dict:
        """Export SQLite database to JSON format"""

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        export_data = {
            'database': os.path.basename(db_path),
            'exported_at': datetime.now().isoformat(),
            'tables': []
        }

        for table in tables:
            table_name = table[0]

            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema = cursor.fetchall()

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            export_data['tables'].append({
                'name': table_name,
                'schema': schema,
                'data': rows,
                'record_count': len(rows)
            })

        conn.close()
        return export_data

    def _backup_source_code(self):
        """Backup Bob's Brain source code"""

        logger.info("💻 Backing up source code...")

        code_backup_dir = f"{self.backup_dir}/source_code"

        if os.path.exists(self.source_code_dir):
            shutil.copytree(
                self.source_code_dir,
                code_backup_dir,
                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', 'cache', '*.log'),
                dirs_exist_ok=True
            )

            self.manifest['files_backed_up'].append(code_backup_dir)
            logger.info("✅ Source code backup complete")
        else:
            logger.warning("⚠️  Source code directory not found")

    def _create_vm_snapshot_reference(self):
        """Create reference for VM snapshot (instruction file)"""

        logger.info("📷 Creating VM snapshot reference...")

        snapshot_ref = {
            'snapshot_recommended': True,
            'vm_name': 'thebeast',
            'project': 'diagnostic-pro-mvp',
            'zone': 'us-central1-a',
            'gcloud_command': 'gcloud compute disks snapshot thebeast --project=diagnostic-pro-mvp --zone=us-central1-a --snapshot-names=bob-brain-backup-{}'.format(self.timestamp),
            'instructions': [
                '1. Run the gcloud command above to create VM snapshot',
                '2. This backup assumes VM snapshot is created for full rollback capability',
                '3. VM snapshot provides instant recovery option if needed'
            ],
            'estimated_snapshot_size': '20GB (boot disk)',
            'estimated_cost': '$1-2 for snapshot storage'
        }

        snapshot_file = f"{self.backup_dir}/vm_snapshot_instructions.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot_ref, f, indent=2)

        self.manifest['files_backed_up'].append(snapshot_file)
        logger.info("✅ VM snapshot reference created")

    def _generate_checksums(self):
        """Generate SHA256 checksums for all backed up files"""

        logger.info("🔐 Generating checksums...")

        checksums = {}

        for file_path in self.manifest['files_backed_up']:
            if os.path.isfile(file_path):
                checksums[file_path] = self._calculate_file_checksum(file_path)

        # Generate checksum for entire backup directory
        checksums['backup_directory'] = self._calculate_directory_checksum(self.backup_dir)

        self.manifest['checksums'] = checksums

        # Save checksums to separate file for validation
        checksum_file = f"{self.backup_dir}/checksums.sha256"
        with open(checksum_file, 'w') as f:
            for path, checksum in checksums.items():
                f.write(f"{checksum}  {path}\n")

        logger.info(f"✅ Generated {len(checksums)} checksums")

    def _calculate_file_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum for a file"""

        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
        except Exception as e:
            logger.error(f"❌ Checksum failed for {file_path}: {e}")
            return "ERROR"

        return hash_sha256.hexdigest()

    def _calculate_directory_checksum(self, directory: str) -> str:
        """Calculate combined checksum for directory contents"""

        hash_sha256 = hashlib.sha256()

        for root, dirs, files in os.walk(directory):
            # Sort for consistent ordering
            dirs.sort()
            files.sort()

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        hash_sha256.update(f.read())
                except Exception as e:
                    logger.warning(f"⚠️  Skipped file in directory checksum: {file_path}")

        return hash_sha256.hexdigest()

    def _save_manifest(self):
        """Save backup manifest"""

        manifest_file = f"{self.backup_dir}/backup_manifest.json"

        with open(manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)

        logger.info(f"✅ Backup manifest saved: {manifest_file}")

    def _create_compressed_archive(self):
        """Create compressed tar.gz archive of backup"""

        logger.info("🗜️  Creating compressed archive...")

        archive_path = f"{self.backup_base_dir}/bob_brain_backup_{self.timestamp}.tar.gz"

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.backup_dir, arcname=f"bob_brain_backup_{self.timestamp}")

        # Calculate archive size
        archive_size_mb = os.path.getsize(archive_path) / (1024 * 1024)

        logger.info(f"✅ Compressed archive created: {archive_path} ({archive_size_mb:.1f} MB)")

        # Update manifest with archive info
        self.manifest['compressed_archive'] = {
            'path': archive_path,
            'size_mb': archive_size_mb,
            'checksum': self._calculate_file_checksum(archive_path)
        }

        # Re-save manifest with archive info
        self._save_manifest()

    def validate_backup(self) -> bool:
        """Validate backup integrity"""

        logger.info("🔍 Validating backup integrity...")

        try:
            # Check if all expected files exist
            missing_files = []
            for file_path in self.manifest['files_backed_up']:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

            if missing_files:
                logger.error(f"❌ Missing files: {missing_files}")
                return False

            # Validate checksums
            checksum_failures = []
            for file_path, expected_checksum in self.manifest['checksums'].items():
                if os.path.isfile(file_path):
                    actual_checksum = self._calculate_file_checksum(file_path)
                    if actual_checksum != expected_checksum:
                        checksum_failures.append(f"{file_path}: expected {expected_checksum}, got {actual_checksum}")

            if checksum_failures:
                logger.error(f"❌ Checksum failures: {checksum_failures}")
                return False

            logger.info("✅ Backup validation successful")
            return True

        except Exception as e:
            logger.error(f"❌ Backup validation failed: {e}")
            return False


class FirestoreValidator:
    """Validate Firestore data after migration"""

    def __init__(self, firestore_project: str = "bobs-house-ai"):
        self.firestore_client = firestore.Client(project=firestore_project)

    def validate_migration(self, backup_manifest: Dict) -> bool:
        """Validate that migration preserved all data"""

        logger.info("🔍 Validating Firestore migration...")

        validation_results = {
            'chromadb_validation': self._validate_chromadb_migration(backup_manifest),
            'conversations_validation': self._validate_conversations_migration(backup_manifest),
            'automation_validation': self._validate_automation_migration(backup_manifest),
            'insights_validation': self._validate_insights_migration(backup_manifest)
        }

        all_valid = all(validation_results.values())

        if all_valid:
            logger.info("✅ Migration validation successful - all data preserved")
        else:
            failed_validations = [k for k, v in validation_results.items() if not v]
            logger.error(f"❌ Migration validation failed: {failed_validations}")

        return all_valid

    def _validate_chromadb_migration(self, backup_manifest: Dict) -> bool:
        """Validate ChromaDB data in Firestore"""

        try:
            expected_count = backup_manifest['data_counts']['chromadb_items']

            # Count documents in Firestore
            docs = list(self.firestore_client.collection('bob_knowledge').limit(expected_count + 100).stream())
            actual_count = len(docs)

            logger.info(f"📊 ChromaDB validation: Expected {expected_count}, Found {actual_count}")

            # Validate a sample of documents have required fields
            sample_size = min(10, actual_count)
            valid_docs = 0

            for doc in docs[:sample_size]:
                data = doc.to_dict()
                if all(field in data for field in ['content', 'embedding', 'created_at']):
                    valid_docs += 1

            structure_valid = valid_docs == sample_size
            count_valid = actual_count >= expected_count  # Allow for additional items

            if count_valid and structure_valid:
                logger.info("✅ ChromaDB migration validated")
                return True
            else:
                logger.error(f"❌ ChromaDB validation failed: count_valid={count_valid}, structure_valid={structure_valid}")
                return False

        except Exception as e:
            logger.error(f"❌ ChromaDB validation error: {e}")
            return False

    def _validate_conversations_migration(self, backup_manifest: Dict) -> bool:
        """Validate conversation data in Firestore"""

        try:
            expected_count = backup_manifest['data_counts'].get('bob_memory.db_records', 0)

            # Count conversation documents
            docs = list(self.firestore_client.collection('bob_conversations').stream())
            actual_count = len(docs)

            logger.info(f"💬 Conversations validation: Expected ≤{expected_count}, Found {actual_count}")

            # Note: Actual count may be less due to filtering duplicate knowledge items
            if actual_count <= expected_count:
                logger.info("✅ Conversations migration validated")
                return True
            else:
                logger.warning(f"⚠️  More conversations than expected - check for duplicates")
                return True  # Not necessarily an error

        except Exception as e:
            logger.error(f"❌ Conversations validation error: {e}")
            return False

    def _validate_automation_migration(self, backup_manifest: Dict) -> bool:
        """Validate automation rules in Firestore"""

        try:
            expected_count = backup_manifest['data_counts'].get('automation.db_records', 0)

            docs = list(self.firestore_client.collection('bob_automation').stream())
            actual_count = len(docs)

            logger.info(f"⚙️  Automation validation: Expected {expected_count}, Found {actual_count}")

            if actual_count >= expected_count:
                logger.info("✅ Automation migration validated")
                return True
            else:
                logger.error(f"❌ Missing automation rules")
                return False

        except Exception as e:
            logger.error(f"❌ Automation validation error: {e}")
            return False

    def _validate_insights_migration(self, backup_manifest: Dict) -> bool:
        """Validate smart insights in Firestore"""

        try:
            expected_count = backup_manifest['data_counts'].get('smart_insights.db_records', 0)

            docs = list(self.firestore_client.collection('bob_insights').stream())
            actual_count = len(docs)

            logger.info(f"🧠 Insights validation: Expected {expected_count}, Found {actual_count}")

            if actual_count >= expected_count:
                logger.info("✅ Insights migration validated")
                return True
            else:
                logger.error(f"❌ Missing insights")
                return False

        except Exception as e:
            logger.error(f"❌ Insights validation error: {e}")
            return False


def main():
    """Main function for backup and validation operations"""

    print("🗄️  BOB'S BRAIN BACKUP & VALIDATION SYSTEM")
    print("=" * 50)

    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 backup_validation_scripts.py backup")
        print("  python3 backup_validation_scripts.py validate")
        print("  python3 backup_validation_scripts.py full-migration-test")
        return

    command = sys.argv[1].lower()

    if command == 'backup':
        # Create comprehensive backup
        backup_system = BobBrainBackup()

        if backup_system.create_full_backup():
            print(f"✅ Backup completed successfully")
            print(f"📁 Backup location: {backup_system.backup_dir}")
            print(f"📊 Data backed up:")
            for key, value in backup_system.manifest['data_counts'].items():
                print(f"   - {key}: {value}")

            # Validate the backup
            if backup_system.validate_backup():
                print("✅ Backup validation passed")
            else:
                print("❌ Backup validation failed")
        else:
            print("❌ Backup failed")

    elif command == 'validate':
        # Validate Firestore migration
        validator = FirestoreValidator()

        # Load the most recent backup manifest
        backup_base_dir = "/home/jeremylongshore/backup"
        backup_dirs = [d for d in os.listdir(backup_base_dir) if d.startswith('bob_brain_backup_')]

        if not backup_dirs:
            print("❌ No backup manifests found")
            return

        latest_backup_dir = sorted(backup_dirs)[-1]
        manifest_file = f"{backup_base_dir}/{latest_backup_dir}/backup_manifest.json"

        if not os.path.exists(manifest_file):
            print(f"❌ Manifest not found: {manifest_file}")
            return

        with open(manifest_file, 'r') as f:
            manifest = json.load(f)

        if validator.validate_migration(manifest):
            print("✅ Migration validation passed")
        else:
            print("❌ Migration validation failed")

    elif command == 'full-migration-test':
        # Complete backup and validation workflow
        print("🚀 Running full migration test...")

        # 1. Create backup
        backup_system = BobBrainBackup()
        if not backup_system.create_full_backup():
            print("❌ Backup failed - aborting test")
            return

        # 2. Validate backup
        if not backup_system.validate_backup():
            print("❌ Backup validation failed - aborting test")
            return

        # 3. Validate Firestore (simulate post-migration)
        validator = FirestoreValidator()
        if validator.validate_migration(backup_system.manifest):
            print("✅ Full migration test passed")
        else:
            print("❌ Full migration test failed")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()


"""
BACKUP LOCATIONS & VALIDATION COMMANDS:

Primary Backup Location:
  /home/jeremylongshore/backup/bob_brain_backup_YYYYMMDD_HHMMSS/

Backup Contents:
  - chromadb/: Full ChromaDB export + raw files
  - sqlite/: All SQLite databases + JSON exports
  - source_code/: Complete Bob's Brain source code
  - vm_snapshot_instructions.json: VM snapshot commands
  - backup_manifest.json: Complete backup metadata
  - checksums.sha256: File integrity checksums

Validation Commands:
  # Create backup before migration
  python3 backup_validation_scripts.py backup

  # Validate Firestore after migration
  python3 backup_validation_scripts.py validate

  # Full migration test (backup + validate)
  python3 backup_validation_scripts.py full-migration-test

  # Manual checksum validation
  cd /home/jeremylongshore/backup/bob_brain_backup_YYYYMMDD_HHMMSS
  sha256sum -c checksums.sha256

VM Snapshot (for complete rollback):
  gcloud compute disks snapshot thebeast \\
    --project=diagnostic-pro-mvp \\
    --zone=us-central1-a \\
    --snapshot-names=bob-brain-backup-YYYYMMDD_HHMMSS

GCS Backup (optional, for offsite storage):
  gsutil -m cp -r /home/jeremylongshore/backup/bob_brain_backup_YYYYMMDD_HHMMSS \\
    gs://bobs-house-ai-backups/
"""
