#!/usr/bin/env python3
"""
Technical Service Bulletin (TSB) Scraper
Scrapes TSBs, recalls, and service bulletins for equipment and vehicles
Uses open-source libraries for web scraping
"""

import asyncio
import hashlib
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)


class TSBScraper:
    """
    Scrapes Technical Service Bulletins from various sources
    Focuses on compact equipment, diesel trucks, and construction machinery
    """

    def __init__(self, project_id="bobs-house-ai", use_neo4j=False):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.use_neo4j = use_neo4j
        self.neo4j_driver = None

        if use_neo4j:
            self._init_neo4j()

        # TSB sources (public/free sources only)
        self.sources = {
            "nhtsa": {
                "name": "NHTSA Safety Issues & Recalls",
                "base_url": "https://www.nhtsa.gov/recalls",
                "api_url": "https://api.nhtsa.gov/products/vehicle/recalls",
                "type": "api",
            },
            "equipment_manufacturers": [
                {
                    "manufacturer": "Bobcat",
                    "url": "https://www.bobcat.com/na/en/support/safety-notices",
                    "type": "static",
                },
                {
                    "manufacturer": "Caterpillar",
                    "url": "https://www.cat.com/en_US/support/safety.html",
                    "type": "static",
                },
                {
                    "manufacturer": "John Deere",
                    "url": "https://www.deere.com/en/parts-and-service/recalls/",
                    "type": "static",
                },
                {
                    "manufacturer": "Kubota",
                    "url": "https://www.kubotausa.com/service-and-support/safety",
                    "type": "static",
                },
            ],
            "forums_tsb": [
                {
                    "name": "TractorByNet Forums",
                    "url": "https://www.tractorbynet.com/forums/",
                    "search": "service bulletin",
                    "type": "forum",
                },
                {
                    "name": "HeavyEquipmentForums",
                    "url": "https://www.heavyequipmentforums.com/",
                    "search": "TSB recall",
                    "type": "forum",
                },
            ],
            "diesel_truck_tsb": [
                {
                    "manufacturer": "Ford",
                    "models": ["F-250", "F-350", "F-450"],
                    "engine": "PowerStroke",
                    "years": "2017-2024",
                },
                {"manufacturer": "RAM", "models": ["2500", "3500"], "engine": "Cummins", "years": "2019-2024"},
                {
                    "manufacturer": "Chevrolet/GMC",
                    "models": ["Silverado 2500", "Sierra 2500"],
                    "engine": "Duramax",
                    "years": "2020-2024",
                },
            ],
        }

        self._ensure_tables()
        logger.info("📋 TSB Scraper initialized")

    def _init_neo4j(self):
        """Initialize Neo4j connection for graph storage"""
        try:
            uri = "bolt://10.128.0.2:7687"
            self.neo4j_driver = GraphDatabase.driver(uri, auth=("neo4j", "BobBrain2025"))
            logger.info("✅ Connected to Neo4j for TSB graph storage")
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            self.use_neo4j = False

    def _ensure_tables(self):
        """Create BigQuery tables for TSB content"""
        dataset_id = f"{self.project_id}.tsb_knowledge"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except Exception:
            pass

        # Schema for TSBs
        schema = [
            bigquery.SchemaField("tsb_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tsb_number", "STRING"),
            bigquery.SchemaField("manufacturer", "STRING"),
            bigquery.SchemaField("model", "STRING"),
            bigquery.SchemaField("year", "STRING"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("affected_systems", "STRING", mode="REPEATED"),
            bigquery.SchemaField("symptoms", "STRING"),
            bigquery.SchemaField("solution", "STRING"),
            bigquery.SchemaField("parts_required", "STRING", mode="REPEATED"),
            bigquery.SchemaField("labor_hours", "FLOAT64"),
            bigquery.SchemaField("severity", "STRING"),  # critical, important, routine
            bigquery.SchemaField("source_url", "STRING"),
            bigquery.SchemaField("issue_date", "DATE"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{dataset_id}.service_bulletins"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info("✅ TSB table ready")
        except Exception:
            pass

    async def scrape_nhtsa_recalls(self, make: str, model: str = None, year: int = None) -> List[Dict]:
        """
        Scrape NHTSA recalls and TSBs using their public API
        """
        recalls = []

        try:
            # Build API URL
            base_url = "https://api.nhtsa.gov/recalls/recallsByVehicle"
            params = {"make": make}
            if model:
                params["model"] = model
            if year:
                params["modelYear"] = year

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()

                for recall in data.get("results", []):
                    tsb_data = {
                        "tsb_number": recall.get("NHTSACampaignNumber", ""),
                        "manufacturer": recall.get("Manufacturer", make),
                        "model": recall.get("Model", model or ""),
                        "year": str(recall.get("ModelYear", year or "")),
                        "title": recall.get("Component", ""),
                        "description": recall.get("Summary", ""),
                        "symptoms": recall.get("Conequence", ""),  # Note: API typo
                        "solution": recall.get("Remedy", ""),
                        "severity": "critical" if "safety" in recall.get("Summary", "").lower() else "important",
                        "issue_date": recall.get("ReportReceivedDate", ""),
                    }
                    recalls.append(tsb_data)

                logger.info(f"✅ Found {len(recalls)} recalls for {make} {model or ''}")

        except Exception as e:
            logger.error(f"NHTSA API error: {e}")

        return recalls

    async def scrape_manufacturer_site(self, manufacturer_info: Dict) -> List[Dict]:
        """
        Scrape manufacturer website for service bulletins
        """
        bulletins = []

        try:
            response = requests.get(
                manufacturer_info["url"], headers={"User-Agent": "Mozilla/5.0 BobBrain TSB Scraper"}
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Look for bulletin patterns
                bulletin_patterns = [
                    soup.find_all("div", class_=re.compile("bulletin|tsb|notice|recall", re.I)),
                    soup.find_all("article", class_=re.compile("service|safety", re.I)),
                    soup.find_all(["li", "tr"], string=re.compile("TSB|bulletin|recall", re.I)),
                ]

                for pattern_results in bulletin_patterns:
                    for element in pattern_results[:10]:  # Limit to 10 per pattern
                        text = element.get_text(strip=True)

                        if len(text) > 50:  # Filter out navigation items
                            tsb_data = self._extract_tsb_info(text, manufacturer_info["manufacturer"])
                            if tsb_data:
                                tsb_data["source_url"] = manufacturer_info["url"]
                                bulletins.append(tsb_data)

                logger.info(f"✅ Found {len(bulletins)} bulletins from {manufacturer_info['manufacturer']}")

        except Exception as e:
            logger.error(f"Manufacturer site error: {e}")

        return bulletins

    def _extract_tsb_info(self, text: str, manufacturer: str) -> Optional[Dict]:
        """
        Extract TSB information from text using patterns
        """
        try:
            # Common TSB patterns
            tsb_patterns = {
                "tsb_number": r"(?:TSB|Bulletin|SB)[:\s#-]*(\d{2,4}-\d{2,4}|\w{2,10})",
                "model": r"(?:Model|Equipment)[:\s]*([\w\s-]+)",
                "year": r"(\d{4})(?:\s*-\s*\d{4})?",
                "system": r"(?:System|Component)[:\s]*([\w\s]+)",
            }

            extracted = {"manufacturer": manufacturer}

            for field, pattern in tsb_patterns.items():
                match = re.search(pattern, text, re.I)
                if match:
                    extracted[field] = match.group(1).strip()

            # Extract symptoms and solutions
            if "symptom" in text.lower() or "problem" in text.lower():
                extracted["symptoms"] = text[:500]

            if "solution" in text.lower() or "repair" in text.lower():
                extracted["solution"] = text[:500]

            # Only return if we have meaningful data
            if len(extracted) > 2:
                return extracted

        except Exception as e:
            logger.debug(f"Extract error: {e}")

        return None

    def extract_affected_systems(self, text: str) -> List[str]:
        """
        Extract affected systems from TSB text
        """
        systems = []

        system_keywords = {
            "engine": ["engine", "motor", "turbo", "injector"],
            "transmission": ["transmission", "gear", "clutch"],
            "hydraulic": ["hydraulic", "pump", "cylinder", "valve"],
            "electrical": ["electrical", "battery", "alternator", "wiring"],
            "emissions": ["dpf", "def", "egr", "emission"],
            "cooling": ["cooling", "radiator", "thermostat"],
            "fuel": ["fuel", "tank", "pump", "injector"],
            "brake": ["brake", "abs", "caliper"],
        }

        text_lower = text.lower()
        for system, keywords in system_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                systems.append(system)

        return systems

    async def store_tsb(self, tsb_data: Dict) -> bool:
        """
        Store TSB in BigQuery and optionally Neo4j
        """
        try:
            # Generate unique ID
            tsb_id = hashlib.md5(
                f"{tsb_data.get('manufacturer', '')}{tsb_data.get('tsb_number', '')}{datetime.now()}".encode()
            ).hexdigest()

            # Extract affected systems
            affected_systems = self.extract_affected_systems(
                f"{tsb_data.get('description', '')} {tsb_data.get('symptoms', '')}"
            )

            # Prepare record
            record = {
                "tsb_id": tsb_id,
                "tsb_number": tsb_data.get("tsb_number", ""),
                "manufacturer": tsb_data.get("manufacturer", ""),
                "model": tsb_data.get("model", ""),
                "year": tsb_data.get("year", ""),
                "title": tsb_data.get("title", "")[:500],
                "description": tsb_data.get("description", "")[:2000],
                "affected_systems": affected_systems,
                "symptoms": tsb_data.get("symptoms", "")[:1000],
                "solution": tsb_data.get("solution", "")[:2000],
                "parts_required": tsb_data.get("parts_required", []),
                "labor_hours": tsb_data.get("labor_hours"),
                "severity": tsb_data.get("severity", "routine"),
                "source_url": tsb_data.get("source_url", ""),
                "issue_date": tsb_data.get("issue_date"),
                "scraped_at": datetime.now(),
            }

            # Store in BigQuery
            table_id = f"{self.project_id}.tsb_knowledge.service_bulletins"
            errors = self.bq_client.insert_rows_json(table_id, [record])

            if errors:
                logger.error(f"BigQuery insert error: {errors}")
                return False

            # Store in Neo4j if enabled
            if self.use_neo4j and self.neo4j_driver:
                await self._store_in_neo4j(record)

            logger.info(f"✅ Stored TSB: {tsb_data.get('tsb_number', tsb_id)}")
            return True

        except Exception as e:
            logger.error(f"Failed to store TSB: {e}")
            return False

    async def _store_in_neo4j(self, record: Dict):
        """Store TSB in Neo4j graph"""
        try:
            with self.neo4j_driver.session() as session:
                query = """
                MERGE (t:TSB {tsb_id: $tsb_id})
                SET t.number = $tsb_number,
                    t.manufacturer = $manufacturer,
                    t.model = $model,
                    t.year = $year,
                    t.title = $title,
                    t.description = $description,
                    t.severity = $severity,
                    t.scraped_at = datetime($scraped_at)

                WITH t
                UNWIND $systems as system
                MERGE (s:System {name: system})
                MERGE (t)-[:AFFECTS]->(s)

                WITH t
                MERGE (m:Manufacturer {name: $manufacturer})
                MERGE (t)-[:ISSUED_BY]->(m)
                """

                session.run(
                    query,
                    tsb_id=record["tsb_id"],
                    tsb_number=record["tsb_number"],
                    manufacturer=record["manufacturer"],
                    model=record["model"],
                    year=record["year"],
                    title=record["title"],
                    description=record["description"][:500],
                    severity=record["severity"],
                    systems=record["affected_systems"],
                    scraped_at=record["scraped_at"].isoformat(),
                )

                logger.info(f"✅ Stored TSB in Neo4j: {record['tsb_number']}")

        except Exception as e:
            logger.error(f"Neo4j storage failed: {e}")

    async def scrape_equipment_tsbs(self):
        """
        Scrape TSBs for all configured equipment manufacturers
        """
        total_scraped = 0

        # Scrape manufacturer sites
        for manufacturer_info in self.sources["equipment_manufacturers"]:
            logger.info(f"📊 Scraping {manufacturer_info['manufacturer']} TSBs...")

            bulletins = await self.scrape_manufacturer_site(manufacturer_info)

            for bulletin in bulletins:
                success = await self.store_tsb(bulletin)
                if success:
                    total_scraped += 1

            await asyncio.sleep(2)  # Rate limiting

        return total_scraped

    async def scrape_diesel_truck_tsbs(self):
        """
        Scrape TSBs for diesel trucks using NHTSA API
        """
        total_scraped = 0

        for truck_info in self.sources["diesel_truck_tsb"]:
            manufacturer = truck_info["manufacturer"]

            for model in truck_info["models"]:
                logger.info(f"📊 Searching TSBs for {manufacturer} {model}...")

                # Get TSBs from NHTSA
                recalls = await self.scrape_nhtsa_recalls(manufacturer, model)

                for recall in recalls:
                    recall["model"] = model
                    recall["manufacturer"] = manufacturer
                    success = await self.store_tsb(recall)
                    if success:
                        total_scraped += 1

                await asyncio.sleep(2)  # Rate limiting

        return total_scraped

    async def search_forums_for_tsbs(self, search_term: str = "service bulletin"):
        """
        Search forums for TSB discussions
        """
        found_tsbs = []

        for forum in self.sources["forums_tsb"]:
            try:
                # Simple search URL construction
                search_url = f"{forum['url']}search/?q={search_term}"

                response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0 BobBrain TSB Scraper"})

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Look for search results
                    results = soup.find_all(["div", "li"], class_=re.compile("result|post|thread", re.I))

                    for result in results[:10]:
                        text = result.get_text(strip=True)

                        # Look for TSB patterns
                        if re.search(r"TSB|bulletin|recall", text, re.I):
                            tsb_info = self._extract_tsb_info(text, "Forum Discussion")
                            if tsb_info:
                                tsb_info["source_url"] = search_url
                                found_tsbs.append(tsb_info)

                logger.info(f"✅ Found {len(found_tsbs)} TSB discussions in {forum['name']}")

            except Exception as e:
                logger.error(f"Forum search error: {e}")

        return found_tsbs


async def main():
    """Test the TSB scraper"""
    logging.basicConfig(level=logging.INFO)

    scraper = TSBScraper(use_neo4j=False)

    print("=" * 60)
    print("📋 TECHNICAL SERVICE BULLETIN SCRAPER")
    print(f"📅 {datetime.now()}")
    print("=" * 60)

    # Test NHTSA API for Ford diesel trucks
    print("\n🔍 Searching for Ford F-350 TSBs...")
    recalls = await scraper.scrape_nhtsa_recalls("Ford", "F-350")
    print(f"Found {len(recalls)} recalls/TSBs")

    for recall in recalls[:3]:
        await scraper.store_tsb(recall)

    # Scrape equipment manufacturers
    print("\n🔍 Scraping equipment manufacturer TSBs...")
    equipment_count = await scraper.scrape_equipment_tsbs()
    print(f"✅ Scraped {equipment_count} equipment TSBs")

    # Scrape diesel truck TSBs
    print("\n🔍 Scraping diesel truck TSBs...")
    truck_count = await scraper.scrape_diesel_truck_tsbs()
    print(f"✅ Scraped {truck_count} truck TSBs")

    print("\n📊 Data stored in BigQuery: tsb_knowledge.service_bulletins")


if __name__ == "__main__":
    asyncio.run(main())
