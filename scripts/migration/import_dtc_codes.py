#!/usr/bin/env python3
"""
Import open source DTC codes into BigQuery
Uses multiple sources for comprehensive coverage
"""

import json
import csv
import logging
from datetime import datetime
import requests
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DTCImporter:
    def __init__(self):
        self.bq_client = bigquery.Client(project="bobs-house-ai")
        self.dataset_id = "knowledge_base"
        self.table_id = f"bobs-house-ai.{self.dataset_id}.dtc_codes"
        
    def create_dtc_table(self):
        """Create DTC codes table in BigQuery"""
        schema = [
            bigquery.SchemaField("code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("system", "STRING"),
            bigquery.SchemaField("manufacturer", "STRING"),
            bigquery.SchemaField("severity", "STRING"),
            bigquery.SchemaField("common_causes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("common_fixes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("import_timestamp", "TIMESTAMP"),
        ]
        
        table = bigquery.Table(self.table_id, schema=schema)
        table = self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"Created/verified table {self.table_id}")
        return table
        
    def import_from_github_csv(self):
        """Import DTC codes from mytrile/obd-trouble-codes CSV"""
        url = "https://raw.githubusercontent.com/mytrile/obd-trouble-codes/master/obd-trouble-codes.csv"
        
        try:
            logger.info("Fetching DTC codes from GitHub CSV...")
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse CSV
            lines = response.text.strip().split('\n')
            reader = csv.DictReader(lines)
            
            records = []
            for row in reader:
                # Determine category and system from code prefix
                code = row.get('code', '')
                category = self.get_category(code)
                system = self.get_system(code)
                
                record = {
                    'code': code,
                    'description': row.get('description', ''),
                    'category': category,
                    'system': system,
                    'manufacturer': 'Generic' if code[1] == '0' else 'Manufacturer Specific',
                    'severity': self.determine_severity(code),
                    'common_causes': self.get_common_causes(code),
                    'common_fixes': self.get_common_fixes(code),
                    'source': 'mytrile/obd-trouble-codes',
                    'import_timestamp': datetime.utcnow().isoformat()
                }
                records.append(record)
            
            logger.info(f"Parsed {len(records)} DTC codes from CSV")
            return records
            
        except Exception as e:
            logger.error(f"Error importing from CSV: {e}")
            return []
    
    def import_from_github_json(self):
        """Import DTC codes from wzr1337's complete list"""
        url = "https://gist.githubusercontent.com/wzr1337/8af2731a5ffa98f9d506537279da7a0e/raw"
        
        try:
            logger.info("Fetching DTC codes from GitHub Gist...")
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse JSON
            data = response.json()
            
            records = []
            for code, description in data.items():
                category = self.get_category(code)
                system = self.get_system(code)
                
                record = {
                    'code': code,
                    'description': description,
                    'category': category,
                    'system': system,
                    'manufacturer': 'Generic' if len(code) > 1 and code[1] == '0' else 'Manufacturer Specific',
                    'severity': self.determine_severity(code),
                    'common_causes': self.get_common_causes(code),
                    'common_fixes': self.get_common_fixes(code),
                    'source': 'wzr1337/complete-dtc-list',
                    'import_timestamp': datetime.utcnow().isoformat()
                }
                records.append(record)
            
            logger.info(f"Parsed {len(records)} DTC codes from JSON")
            return records
            
        except Exception as e:
            logger.error(f"Error importing from JSON: {e}")
            return []
    
    def get_category(self, code):
        """Determine category from DTC code prefix"""
        if not code:
            return "Unknown"
        
        prefix = code[0].upper()
        categories = {
            'P': 'Powertrain',
            'B': 'Body',
            'C': 'Chassis',
            'U': 'Network/Communication'
        }
        return categories.get(prefix, 'Unknown')
    
    def get_system(self, code):
        """Determine system from DTC code"""
        if not code or len(code) < 3:
            return "Unknown"
        
        if code[0] == 'P':
            if code[2] == '0':
                return "Fuel and Air Metering"
            elif code[2] == '1':
                return "Fuel and Air Metering"
            elif code[2] == '2':
                return "Fuel and Air Metering (Injector)"
            elif code[2] == '3':
                return "Ignition System"
            elif code[2] == '4':
                return "Emission Control"
            elif code[2] == '5':
                return "Vehicle Speed Control"
            elif code[2] == '6':
                return "Computer Output Circuit"
            elif code[2] == '7':
                return "Transmission"
            elif code[2] == '8':
                return "Transmission"
        
        return "General"
    
    def determine_severity(self, code):
        """Determine severity based on code patterns"""
        if not code:
            return "Unknown"
        
        # Critical codes that affect drivability
        critical_patterns = ['P0300', 'P0301', 'P0302', 'P0303', 'P0304', 'P0305', 'P0306', 'P0307', 'P0308',
                           'P0171', 'P0172', 'P0174', 'P0175', 'P0087', 'P0088', 'P0230', 'P0231']
        
        # Moderate codes that should be addressed soon
        moderate_patterns = ['P0420', 'P0430', 'P0401', 'P0402', 'P0403', 'P0404', 'P0405',
                            'P0440', 'P0441', 'P0442', 'P0443', 'P0444', 'P0445', 'P0446']
        
        for pattern in critical_patterns:
            if code.startswith(pattern):
                return "Critical"
        
        for pattern in moderate_patterns:
            if code.startswith(pattern):
                return "Moderate"
        
        return "Low"
    
    def get_common_causes(self, code):
        """Get common causes for specific DTC codes"""
        common_causes = {
            'P0300': ['Faulty spark plugs', 'Bad ignition coils', 'Vacuum leak', 'Low fuel pressure'],
            'P0420': ['Faulty catalytic converter', 'Oxygen sensor failure', 'Exhaust leak', 'Engine misfire'],
            'P0171': ['Vacuum leak', 'Faulty MAF sensor', 'Clogged fuel filter', 'Weak fuel pump'],
            'P0401': ['Clogged EGR passages', 'Faulty EGR valve', 'Carbon buildup', 'Vacuum hose leak'],
            'P0440': ['Loose gas cap', 'EVAP leak', 'Faulty purge valve', 'Damaged EVAP lines'],
        }
        
        # Return specific causes if available, otherwise generic based on category
        for key in common_causes:
            if code.startswith(key):
                return common_causes[key]
        
        return ['Sensor failure', 'Wiring issue', 'Control module fault']
    
    def get_common_fixes(self, code):
        """Get common fixes for specific DTC codes"""
        common_fixes = {
            'P0300': ['Replace spark plugs', 'Replace ignition coils', 'Fix vacuum leaks', 'Clean fuel injectors'],
            'P0420': ['Replace catalytic converter', 'Replace O2 sensors', 'Fix exhaust leaks', 'Use catalytic converter cleaner'],
            'P0171': ['Find and fix vacuum leaks', 'Clean or replace MAF sensor', 'Replace fuel filter', 'Test fuel pressure'],
            'P0401': ['Clean EGR passages', 'Replace EGR valve', 'Remove carbon deposits', 'Replace vacuum hoses'],
            'P0440': ['Tighten gas cap', 'Replace gas cap', 'Fix EVAP leaks', 'Replace purge valve'],
        }
        
        for key in common_fixes:
            if code.startswith(key):
                return common_fixes[key]
        
        return ['Diagnose with scanner', 'Check wiring', 'Replace sensor', 'Clear code and retest']
    
    def import_all_sources(self):
        """Import from all available sources"""
        all_records = []
        
        # Import from CSV source
        csv_records = self.import_from_github_csv()
        all_records.extend(csv_records)
        
        # Import from JSON source
        json_records = self.import_from_github_json()
        
        # Merge records, avoiding duplicates
        existing_codes = {r['code'] for r in all_records}
        for record in json_records:
            if record['code'] not in existing_codes:
                all_records.append(record)
        
        logger.info(f"Total unique DTC codes collected: {len(all_records)}")
        
        # Load to BigQuery
        if all_records:
            self.load_to_bigquery(all_records)
        
        return all_records
    
    def load_to_bigquery(self, records):
        """Load DTC codes to BigQuery"""
        try:
            # Create table if not exists
            self.create_dtc_table()
            
            # Insert records
            errors = self.bq_client.insert_rows_json(self.table_id, records)
            
            if errors:
                logger.error(f"BigQuery insert errors: {errors}")
            else:
                logger.info(f"Successfully loaded {len(records)} DTC codes to BigQuery")
                
        except Exception as e:
            logger.error(f"Error loading to BigQuery: {e}")
    
    def add_equipment_specific_codes(self):
        """Add equipment-specific codes for construction/agriculture"""
        equipment_codes = [
            # Bobcat specific
            {'code': 'B0001', 'description': 'Hydraulic pressure sensor circuit', 'category': 'Body', 
             'system': 'Hydraulic', 'manufacturer': 'Bobcat', 'severity': 'Moderate',
             'common_causes': ['Faulty pressure sensor', 'Hydraulic leak', 'Clogged filter'],
             'common_fixes': ['Replace sensor', 'Fix hydraulic leak', 'Replace hydraulic filter'],
             'source': 'Equipment Manual', 'import_timestamp': datetime.utcnow().isoformat()},
            
            # John Deere specific
            {'code': 'JD001', 'description': 'DEF quality sensor fault', 'category': 'Powertrain',
             'system': 'Emission Control', 'manufacturer': 'John Deere', 'severity': 'Critical',
             'common_causes': ['Bad DEF fluid', 'Faulty sensor', 'Contaminated DEF tank'],
             'common_fixes': ['Replace DEF fluid', 'Replace sensor', 'Clean DEF system'],
             'source': 'Equipment Manual', 'import_timestamp': datetime.utcnow().isoformat()},
            
            # Caterpillar specific
            {'code': 'CAT001', 'description': 'Engine oil pressure low', 'category': 'Powertrain',
             'system': 'Engine', 'manufacturer': 'Caterpillar', 'severity': 'Critical',
             'common_causes': ['Low oil level', 'Oil pump failure', 'Clogged oil filter'],
             'common_fixes': ['Add oil', 'Replace oil pump', 'Replace oil filter'],
             'source': 'Equipment Manual', 'import_timestamp': datetime.utcnow().isoformat()},
        ]
        
        self.load_to_bigquery(equipment_codes)
        logger.info(f"Added {len(equipment_codes)} equipment-specific codes")

def main():
    """Main execution"""
    importer = DTCImporter()
    
    # Import from all sources
    records = importer.import_all_sources()
    
    # Add equipment-specific codes
    importer.add_equipment_specific_codes()
    
    logger.info("DTC import complete!")
    
    # Print summary
    print(f"\n✅ Successfully imported DTC codes to BigQuery")
    print(f"📊 Total codes imported: {len(records)}")
    print(f"📍 Location: bobs-house-ai.knowledge_base.dtc_codes")
    print(f"\nYou can query them with:")
    print("bq query --use_legacy_sql=false 'SELECT * FROM `bobs-house-ai.knowledge_base.dtc_codes` LIMIT 10'")

if __name__ == "__main__":
    main()