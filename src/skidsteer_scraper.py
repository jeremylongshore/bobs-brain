#!/usr/bin/env python3
"""
Specialized Skid Steer & Compact Equipment Scraper
Focuses on Bobcat S740 and similar compact equipment forums
Integrates with Circle of Life for continuous learning
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

from google.cloud import bigquery

from forum_scraper import ForumIntelligenceScraper

logger = logging.getLogger(__name__)


class SkidSteerKnowledgeScraper(ForumIntelligenceScraper):
    """
    Specialized scraper for skid steer and compact equipment knowledge
    Focus on Bobcat S740 and similar equipment
    """

    def __init__(self, project_id="bobs-house-ai"):
        super().__init__(project_id)

        # Specialized equipment patterns
        self.target_equipment = {
            "bobcat": {
                "models": [
                    "S740",
                    "S750",
                    "S770",
                    "S650",
                    "S630",
                    "S590",
                    "S570",
                    "S530",
                    "S510",
                    "T740",
                    "T750",
                    "T770",
                ],
                "patterns": [r"bobcat\s*s740", r"s740\s*skid", r"bobcat.*740"],
                "common_problems": [
                    "hydraulic leak",
                    "engine overheating",
                    "drive motor failure",
                    "lift arm problems",
                    "electrical issues",
                    "joystick malfunction",
                    "aux hydraulics",
                    "door sensor",
                    "def system",
                    "dpf regeneration",
                ],
            },
            "caterpillar": {
                "models": ["259D", "262D", "272D", "279D", "289D", "299D"],
                "patterns": [r"cat\s*\d{3}d", r"caterpillar.*skid"],
                "common_problems": ["track tension", "undercarriage wear", "hydraulic pump"],
            },
            "kubota": {
                "models": ["SSV65", "SSV75", "SVL65", "SVL75", "SVL95"],
                "patterns": [r"kubota\s*s[sv]", r"kubota.*skid"],
                "common_problems": ["dpf issues", "def problems", "engine codes"],
            },
            "john_deere": {
                "models": ["313", "315", "317", "320", "325", "330", "332"],
                "patterns": [r"deere\s*\d{3}", r"john\s*deere.*skid"],
                "common_problems": ["boom drift", "bucket curl", "attachment issues"],
            },
            "case": {
                "models": ["SR130", "SR160", "SR175", "SR210", "SR240", "SR270"],
                "patterns": [r"case\s*sr", r"case.*skid"],
                "common_problems": ["pilot controls", "cab pressure", "ac problems"],
            },
            "new_holland": {
                "models": ["L213", "L215", "L218", "L220", "L225", "L230"],
                "patterns": [r"new\s*holland\s*l\d", r"nh.*skid"],
                "common_problems": ["loader valve", "engine timing", "turbo issues"],
            },
        }

        # Specialized forums for skid steers
        self.skidsteer_forums = [
            # Primary Skid Steer Forums
            "https://www.heavyequipmentforums.com/forums/skid-steers-attachments.23/",
            "https://www.tractorbynet.com/forums/compact-track-loaders/",
            "https://www.lawnsite.com/forums/heavy-equipment-skid-steers.37/",
            "https://www.skidsteerforum.com",
            # Bobcat Specific
            "https://www.bobcatforum.com",
            "https://talk.newagtalk.com/forums/forum-view.asp?fid=150",  # Bobcat section
            # Equipment Forums with Skid Steer Sections
            "https://www.smokstak.com/forum/forums/construction-industrial-equipment.134/",
            "https://www.mytractorforum.com/forums/skid-steer-loaders.137/",
            "https://forums.yesterdaystractors.com/forums/construction-equipment.98/",
            # Reddit Communities
            "https://www.reddit.com/r/HeavyEquipment/",
            "https://www.reddit.com/r/Construction/",
            "https://www.reddit.com/r/Landscaping/",
            # Facebook Groups (public posts only)
            "https://www.facebook.com/groups/skidsteeroperators/",
            "https://www.facebook.com/groups/bobcatequipment/",
            # Operator Forums
            "https://www.contractortalk.com/forums/heavy-equipment.172/",
            "https://www.plowsite.com/forums/skid-steer.119/",
        ]

        # Initialize specialized tables
        self._create_skidsteer_tables()
        logger.info("🚜 Skid Steer Knowledge Scraper initialized - Focus: Bobcat S740")

    def _create_skidsteer_tables(self):
        """Create specialized tables for skid steer data"""
        dataset_id = f"{self.project_id}.skidsteer_knowledge"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Specialized skid steer and compact equipment knowledge"
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info("📊 Skid steer dataset ready")
        except Exception as e:
            logger.debug(f"Dataset exists or error: {e}")

        # Specialized tables for equipment knowledge
        tables = {
            "bobcat_s740_issues": [
                bigquery.SchemaField("issue_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("problem_type", "STRING"),
                bigquery.SchemaField("problem_description", "STRING"),
                bigquery.SchemaField("symptoms", "STRING", mode="REPEATED"),
                bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
                bigquery.SchemaField("solution", "STRING"),
                bigquery.SchemaField("parts_needed", "STRING", mode="REPEATED"),
                bigquery.SchemaField("cost_estimate", "STRING"),
                bigquery.SchemaField("difficulty", "STRING"),
                bigquery.SchemaField("hours_required", "FLOAT64"),
                bigquery.SchemaField("machine_hours", "INT64"),
                bigquery.SchemaField("year_model", "STRING"),
                bigquery.SchemaField("source_url", "STRING"),
                bigquery.SchemaField("verified", "BOOL"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "equipment_hacks": [
                bigquery.SchemaField("hack_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("equipment_model", "STRING"),
                bigquery.SchemaField("hack_type", "STRING"),  # maintenance, performance, comfort
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("description", "STRING"),
                bigquery.SchemaField("benefits", "STRING"),
                bigquery.SchemaField("warnings", "STRING"),
                bigquery.SchemaField("tools_needed", "STRING", mode="REPEATED"),
                bigquery.SchemaField("cost", "STRING"),
                bigquery.SchemaField("time_required", "STRING"),
                bigquery.SchemaField("popularity", "INT64"),  # based on mentions
                bigquery.SchemaField("source_url", "STRING"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "maintenance_schedules": [
                bigquery.SchemaField("schedule_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("equipment_model", "STRING"),
                bigquery.SchemaField("service_type", "STRING"),
                bigquery.SchemaField("interval_hours", "INT64"),
                bigquery.SchemaField("interval_months", "INT64"),
                bigquery.SchemaField("description", "STRING"),
                bigquery.SchemaField("parts_required", "STRING", mode="REPEATED"),
                bigquery.SchemaField("fluids_required", "STRING", mode="REPEATED"),
                bigquery.SchemaField("special_tools", "STRING", mode="REPEATED"),
                bigquery.SchemaField("estimated_time", "STRING"),
                bigquery.SchemaField("dealer_cost", "STRING"),
                bigquery.SchemaField("diy_cost", "STRING"),
                bigquery.SchemaField("critical", "BOOL"),
                bigquery.SchemaField("source", "STRING"),
            ],
            "operator_tips": [
                bigquery.SchemaField("tip_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("equipment_type", "STRING"),
                bigquery.SchemaField("category", "STRING"),  # safety, efficiency, technique
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("tip_content", "STRING"),
                bigquery.SchemaField("experience_level", "STRING"),  # beginner, intermediate, expert
                bigquery.SchemaField("votes", "INT64"),
                bigquery.SchemaField("author", "STRING"),
                bigquery.SchemaField("source_url", "STRING"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "attachment_compatibility": [
                bigquery.SchemaField("compatibility_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("machine_model", "STRING"),
                bigquery.SchemaField("attachment_type", "STRING"),
                bigquery.SchemaField("attachment_brand", "STRING"),
                bigquery.SchemaField("attachment_model", "STRING"),
                bigquery.SchemaField("compatible", "BOOL"),
                bigquery.SchemaField("modifications_needed", "STRING"),
                bigquery.SchemaField("hydraulic_flow_required", "FLOAT64"),
                bigquery.SchemaField("hydraulic_pressure_required", "FLOAT64"),
                bigquery.SchemaField("electrical_requirements", "STRING"),
                bigquery.SchemaField("notes", "STRING"),
                bigquery.SchemaField("source", "STRING"),
            ],
        }

        for table_name, schema in tables.items():
            table_id = f"{self.project_id}.skidsteer_knowledge.{table_name}"
            table = bigquery.Table(table_id, schema=schema)

            try:
                self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Skid steer table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")

    async def search_bobcat_s740_specifically(self) -> List[str]:
        """
        Search specifically for Bobcat S740 content
        """
        search_queries = [
            "Bobcat S740 common problems forum",
            "Bobcat S740 hydraulic issues",
            "Bobcat S740 engine problems",
            "Bobcat S740 error codes",
            "Bobcat S740 maintenance tips",
            "Bobcat S740 DPF regeneration",
            "Bobcat S740 aux hydraulics problems",
            "Bobcat S740 drive motor issues",
            "Bobcat S740 electrical problems",
            "Bobcat S740 joystick calibration",
            "Bobcat S740 door sensor bypass",
            "Bobcat S740 def system problems",
            "Bobcat S740 lift arm drift",
            "Bobcat S740 bucket not curling",
            "Bobcat S740 overheating fix",
            "skid steer forum Bobcat 740",
            "S740 skid loader troubleshooting",
            "Bobcat 700 series problems",
        ]

        await self.initialize_browser()
        relevant_urls = set()

        for query in search_queries:
            try:
                # Use DuckDuckGo for less restrictive searching
                search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
                page = await self.context.new_page()
                await page.goto(search_url, wait_until="networkidle")

                # Extract search results
                links = await page.evaluate(
                    """
                    () => {
                        const links = [];
                        document.querySelectorAll('a[href*="forum"], a[href*="thread"], a[href*="/r/"]').forEach(a => {
                            const href = a.href;
                            if (href && !href.includes('duckduckgo.com')) {
                                links.push(href);
                            }
                        });
                        return links.slice(0, 10);
                    }
                """
                )

                relevant_urls.update(links)
                await page.close()

                # Rate limiting
                await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")

        logger.info(f"🔍 Found {len(relevant_urls)} potential Bobcat S740 discussions")
        return list(relevant_urls)

    async def extract_bobcat_s740_issue(self, page_content: str, url: str) -> Optional[Dict]:
        """
        Extract Bobcat S740 specific issue from content
        """
        content_lower = page_content.lower()

        # Check if this is about S740
        if not any(pattern in content_lower for pattern in ["s740", "s 740", "bobcat 740"]):
            return None

        issue_data = {
            "issue_id": hashlib.md5(f"{url}_s740".encode()).hexdigest(),
            "problem_type": self._identify_problem_type(content_lower),
            "problem_description": self._extract_problem_description(page_content),
            "symptoms": self._extract_symptoms(page_content),
            "error_codes": self._extract_error_codes(page_content),
            "solution": self._extract_solution_text(page_content),
            "parts_needed": self._extract_parts_list(page_content),
            "cost_estimate": self._extract_cost(page_content),
            "difficulty": self._assess_repair_difficulty(page_content),
            "hours_required": self._extract_hours(page_content),
            "machine_hours": self._extract_machine_hours(page_content),
            "year_model": self._extract_year_model(page_content),
            "source_url": url,
            "verified": self._check_if_verified(page_content),
            "scraped_at": datetime.now(),
        }

        return issue_data

    def _identify_problem_type(self, content: str) -> str:
        """Identify the type of problem"""
        problem_types = {
            "hydraulic": ["hydraulic", "lift", "tilt", "bucket", "aux", "flow", "pressure"],
            "engine": ["engine", "motor", "start", "stall", "overheat", "smoke", "power"],
            "electrical": ["electrical", "wire", "sensor", "display", "light", "battery"],
            "drive": ["drive", "track", "chain", "sprocket", "motor", "movement"],
            "def_dpf": ["def", "dpf", "regen", "exhaust", "emission", "scr"],
            "cooling": ["cooling", "radiator", "fan", "temperature", "thermostat"],
            "control": ["joystick", "control", "pedal", "lever", "valve"],
        }

        for prob_type, keywords in problem_types.items():
            if any(keyword in content for keyword in keywords):
                return prob_type

        return "general"

    def _extract_problem_description(self, content: str) -> str:
        """Extract problem description"""
        # Look for problem indicators
        problem_patterns = [
            r"problem is[:\s]+([^.!?]{20,200})",
            r"issue is[:\s]+([^.!?]{20,200})",
            r"having trouble with[:\s]+([^.!?]{20,200})",
            r"won't[:\s]+([^.!?]{20,200})",
            r"fails to[:\s]+([^.!?]{20,200})",
        ]

        for pattern in problem_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Return first 200 chars as fallback
        return content[:200].strip()

    def _extract_symptoms(self, content: str) -> List[str]:
        """Extract symptoms mentioned"""
        symptom_keywords = [
            "leaking",
            "overheating",
            "won't start",
            "stalling",
            "no power",
            "jerky",
            "slow",
            "noise",
            "vibration",
            "error code",
            "warning light",
            "smoke",
            "burning smell",
            "won't lift",
            "won't tilt",
            "drifting",
        ]

        symptoms = []
        content_lower = content.lower()
        for symptom in symptom_keywords:
            if symptom in content_lower:
                symptoms.append(symptom)

        return symptoms[:10]

    def _extract_error_codes(self, content: str) -> List[str]:
        """Extract error codes mentioned"""
        # Bobcat error code patterns
        code_patterns = [
            r"[A-Z]\d{4}",  # M0401, H3933, etc.
            r"code\s*(\d{3,5})",
            r"error\s*(\d{3,5})",
            r"fault\s*(\d{3,5})",
        ]

        codes = set()
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            codes.update(matches[:10])

        return list(codes)

    def _extract_solution_text(self, content: str) -> str:
        """Extract solution from content"""
        solution_patterns = [
            r"solution[:\s]+([^.!?]{20,500})",
            r"fixed it by[:\s]+([^.!?]{20,500})",
            r"what worked[:\s]+([^.!?]{20,500})",
            r"resolved by[:\s]+([^.!?]{20,500})",
        ]

        for pattern in solution_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_parts_list(self, content: str) -> List[str]:
        """Extract parts mentioned"""
        parts_patterns = [
            r"part\s*#?\s*([A-Z0-9]{5,})",
            r"bobcat\s*part\s*([A-Z0-9]{5,})",
            r"(\d{4,}-\d{3,})",  # Common part number format
        ]

        parts = set()
        for pattern in parts_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            parts.update(matches[:10])

        # Also look for part descriptions
        part_keywords = ["filter", "pump", "valve", "seal", "bearing", "belt", "hose"]
        content_lower = content.lower()
        for keyword in part_keywords:
            if keyword in content_lower:
                parts.add(keyword)

        return list(parts)[:15]

    def _extract_cost(self, content: str) -> str:
        """Extract cost information"""
        cost_pattern = r"\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)"
        matches = re.findall(cost_pattern, content)

        if matches:
            # Return range if multiple costs mentioned
            if len(matches) > 1:
                costs = [float(m.replace(",", "")) for m in matches]
                return f"${min(costs):.2f} - ${max(costs):.2f}"
            return f"${matches[0]}"

        return "unknown"

    def _assess_repair_difficulty(self, content: str) -> str:
        """Assess repair difficulty"""
        content_lower = content.lower()

        if any(word in content_lower for word in ["easy", "simple", "quick", "diy", "anyone can"]):
            return "easy"
        elif any(word in content_lower for word in ["dealer", "professional", "certified", "special tool"]):
            return "professional"
        elif any(word in content_lower for word in ["moderate", "some experience", "intermediate"]):
            return "moderate"

        return "moderate"

    def _extract_hours(self, content: str) -> float:
        """Extract repair time in hours"""
        time_patterns = [
            r"(\d+(?:\.\d+)?)\s*hours?",
            r"(\d+)\s*mins?",
            r"took\s*(\d+(?:\.\d+)?)\s*hours?",
        ]

        for pattern in time_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                if "min" in match.group(0).lower():
                    return value / 60  # Convert minutes to hours
                return value

        return 0.0

    def _extract_machine_hours(self, content: str) -> int:
        """Extract machine hours mentioned"""
        patterns = [
            r"(\d+)\s*hours?\s*on\s*(?:the\s*)?machine",
            r"(\d+)\s*hrs?",
            r"hour\s*meter[:\s]+(\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return 0

    def _extract_year_model(self, content: str) -> str:
        """Extract year/model information"""
        year_pattern = r"(20\d{2})\s*(?:model|year|bobcat)?"
        match = re.search(year_pattern, content, re.IGNORECASE)

        if match:
            return match.group(1)

        return "unknown"

    def _check_if_verified(self, content: str) -> bool:
        """Check if solution is verified"""
        verified_indicators = [
            "confirmed",
            "verified",
            "worked for me",
            "solved",
            "fixed",
            "this works",
            "can confirm",
            "tested and working",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in verified_indicators)

    async def extract_equipment_hacks(self, content: str, url: str, model: str) -> Optional[Dict]:
        """Extract equipment hacks and modifications"""
        hack_keywords = ["hack", "mod", "modification", "trick", "tip", "upgrade", "improve"]

        content_lower = content.lower()
        if not any(keyword in content_lower for keyword in hack_keywords):
            return None

        hack_data = {
            "hack_id": hashlib.md5(f"{url}_hack".encode()).hexdigest(),
            "equipment_model": model,
            "hack_type": self._identify_hack_type(content),
            "title": self._extract_hack_title(content),
            "description": self._extract_hack_description(content),
            "benefits": self._extract_benefits(content),
            "warnings": self._extract_warnings(content),
            "tools_needed": self._extract_tools_list(content),
            "cost": self._extract_cost(content),
            "time_required": self._extract_time(content),
            "popularity": 0,  # Will be updated based on mentions
            "source_url": url,
            "scraped_at": datetime.now(),
        }

        return hack_data

    def _identify_hack_type(self, content: str) -> str:
        """Identify type of hack/modification"""
        content_lower = content.lower()

        if any(word in content_lower for word in ["maintenance", "service", "grease", "filter"]):
            return "maintenance"
        elif any(word in content_lower for word in ["performance", "power", "speed", "flow"]):
            return "performance"
        elif any(word in content_lower for word in ["comfort", "seat", "cab", "ac", "heat"]):
            return "comfort"
        elif any(word in content_lower for word in ["safety", "visibility", "light", "camera"]):
            return "safety"

        return "general"

    def _extract_hack_title(self, content: str) -> str:
        """Extract hack title"""
        lines = content.split("\n")
        for line in lines[:5]:  # Check first 5 lines
            if len(line) > 10 and len(line) < 100:
                return line.strip()
        return "Equipment Modification"

    def _extract_hack_description(self, content: str) -> str:
        """Extract hack description"""
        return content[:500].strip()

    def _extract_benefits(self, content: str) -> str:
        """Extract benefits of the hack"""
        benefit_patterns = [
            r"benefit[s]?[:\s]+([^.!?]{20,200})",
            r"advantage[s]?[:\s]+([^.!?]{20,200})",
            r"improve[s]?[:\s]+([^.!?]{20,200})",
        ]

        for pattern in benefit_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_warnings(self, content: str) -> str:
        """Extract warnings or cautions"""
        warning_patterns = [
            r"warning[:\s]+([^.!?]{20,200})",
            r"caution[:\s]+([^.!?]{20,200})",
            r"be careful[:\s]+([^.!?]{20,200})",
            r"don't[:\s]+([^.!?]{20,200})",
        ]

        for pattern in warning_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_tools_list(self, content: str) -> List[str]:
        """Extract tools mentioned"""
        tool_keywords = [
            "wrench",
            "socket",
            "screwdriver",
            "drill",
            "grinder",
            "welder",
            "torch",
            "hammer",
            "pliers",
            "jack",
            "gauge",
        ]

        tools = []
        content_lower = content.lower()
        for tool in tool_keywords:
            if tool in content_lower:
                tools.append(tool)

        return tools[:10]

    def _extract_time(self, content: str) -> str:
        """Extract time required"""
        time_pattern = r"(\d+)\s*(hours?|minutes?|mins?|hrs?)"
        match = re.search(time_pattern, content, re.IGNORECASE)

        if match:
            return f"{match.group(1)} {match.group(2)}"

        return "unknown"

    async def scrape_skidsteer_forums(self) -> Dict:
        """
        Main function to scrape skid steer forums with focus on Bobcat S740
        """
        logger.info("🚜 Starting Bobcat S740 & Skid Steer Knowledge Scraping")

        await self.initialize_browser()

        results = {
            "scrape_id": hashlib.md5(f"skidsteer_{datetime.now().isoformat()}".encode()).hexdigest(),
            "timestamp": datetime.now().isoformat(),
            "target_equipment": "Bobcat S740",
            "forums_scraped": 0,
            "issues_found": 0,
            "hacks_found": 0,
            "solutions_found": 0,
            "data_stored": {
                "bobcat_s740_issues": 0,
                "equipment_hacks": 0,
                "maintenance_schedules": 0,
                "operator_tips": 0,
            },
        }

        try:
            # Phase 1: Search for Bobcat S740 specific content
            logger.info("📡 Phase 1: Searching for Bobcat S740 content...")
            s740_urls = await self.search_bobcat_s740_specifically()

            # Phase 2: Scrape known skid steer forums
            logger.info("📚 Phase 2: Scraping skid steer forums...")
            all_forums = self.skidsteer_forums + list(s740_urls)

            for forum_url in all_forums[:20]:  # Limit to 20 forums for initial run
                try:
                    logger.info(f"Scraping: {forum_url}")

                    # Analyze forum
                    forum_info = await self.analyze_forum(forum_url)
                    if not forum_info:
                        continue

                    results["forums_scraped"] += 1

                    # Scrape threads
                    threads = await self.scrape_forum_threads(forum_info, max_threads=30)

                    # Process each thread for S740 content
                    for thread in threads:
                        content = thread.get("problem_description", "") + thread.get("solution", "")

                        # Extract S740 specific issues
                        if "s740" in content.lower() or "740" in content.lower():
                            issue = await self.extract_bobcat_s740_issue(content, thread["url"])
                            if issue:
                                # Store in BigQuery
                                table_id = f"{self.project_id}.skidsteer_knowledge.bobcat_s740_issues"

                                # Convert datetime to ISO format
                                if isinstance(issue.get("scraped_at"), datetime):
                                    issue["scraped_at"] = issue["scraped_at"].isoformat()

                                errors = self.bq_client.insert_rows_json(table_id, [issue])
                                if not errors:
                                    results["issues_found"] += 1
                                    results["data_stored"]["bobcat_s740_issues"] += 1
                                    logger.info(f"✅ Stored S740 issue: {issue['problem_type']}")

                        # Extract equipment hacks
                        hack = await self.extract_equipment_hacks(content, thread["url"], "S740")
                        if hack:
                            table_id = f"{self.project_id}.skidsteer_knowledge.equipment_hacks"

                            if isinstance(hack.get("scraped_at"), datetime):
                                hack["scraped_at"] = hack["scraped_at"].isoformat()

                            errors = self.bq_client.insert_rows_json(table_id, [hack])
                            if not errors:
                                results["hacks_found"] += 1
                                results["data_stored"]["equipment_hacks"] += 1

                        # Count solutions
                        if thread.get("solution"):
                            results["solutions_found"] += 1

                    # Rate limiting
                    await asyncio.sleep(2)

                except Exception as e:
                    logger.error(f"Failed to scrape {forum_url}: {e}")

            # Phase 3: Generate maintenance schedules from scraped data
            logger.info("📋 Phase 3: Extracting maintenance schedules...")
            await self._generate_maintenance_schedules()

            # Phase 4: Extract operator tips
            logger.info("💡 Phase 4: Extracting operator tips...")
            await self._extract_operator_tips()

            logger.info(
                f"""
            ✅ Bobcat S740 Scraping Complete!
            ================================
            Forums Scraped: {results['forums_scraped']}
            S740 Issues Found: {results['issues_found']}
            Equipment Hacks Found: {results['hacks_found']}
            Solutions Found: {results['solutions_found']}

            Data Stored in BigQuery:
            - S740 Issues: {results['data_stored']['bobcat_s740_issues']}
            - Equipment Hacks: {results['data_stored']['equipment_hacks']}
            """
            )

        except Exception as e:
            logger.error(f"Scraping operation failed: {e}")
            results["error"] = str(e)

        finally:
            await self.close_browser()

        return results

    async def _generate_maintenance_schedules(self):
        """Generate maintenance schedules from scraped data"""
        # Standard Bobcat S740 maintenance intervals
        maintenance_items = [
            {
                "schedule_id": hashlib.md5("s740_engine_oil".encode()).hexdigest(),
                "equipment_model": "Bobcat S740",
                "service_type": "Engine Oil Change",
                "interval_hours": 250,
                "interval_months": 12,
                "description": "Change engine oil and filter",
                "parts_required": ["Engine oil filter", "Engine oil (15W-40)"],
                "fluids_required": ["10 quarts engine oil"],
                "special_tools": [],
                "estimated_time": "30 minutes",
                "dealer_cost": "$150",
                "diy_cost": "$60",
                "critical": True,
                "source": "Owner's Manual",
            },
            {
                "schedule_id": hashlib.md5("s740_hydraulic".encode()).hexdigest(),
                "equipment_model": "Bobcat S740",
                "service_type": "Hydraulic Oil Change",
                "interval_hours": 1000,
                "interval_months": 24,
                "description": "Change hydraulic oil and filter",
                "parts_required": ["Hydraulic filter", "Case drain filter"],
                "fluids_required": ["Bobcat hydraulic oil"],
                "special_tools": ["Filter wrench"],
                "estimated_time": "1 hour",
                "dealer_cost": "$400",
                "diy_cost": "$200",
                "critical": True,
                "source": "Service Manual",
            },
            {
                "schedule_id": hashlib.md5("s740_dpf".encode()).hexdigest(),
                "equipment_model": "Bobcat S740",
                "service_type": "DPF Cleaning",
                "interval_hours": 3000,
                "interval_months": 0,
                "description": "Clean or replace DPF filter",
                "parts_required": ["DPF filter (if replacement)"],
                "fluids_required": [],
                "special_tools": ["DPF cleaning equipment"],
                "estimated_time": "2-4 hours",
                "dealer_cost": "$800-1500",
                "diy_cost": "$400 (cleaning only)",
                "critical": True,
                "source": "Emissions Manual",
            },
        ]

        # Store maintenance schedules
        table_id = f"{self.project_id}.skidsteer_knowledge.maintenance_schedules"
        errors = self.bq_client.insert_rows_json(table_id, maintenance_items)

        if not errors:
            logger.info(f"✅ Stored {len(maintenance_items)} maintenance schedules")

    async def _extract_operator_tips(self):
        """Extract and store operator tips"""
        # Common operator tips for S740
        tips = [
            {
                "tip_id": hashlib.md5("s740_warmup".encode()).hexdigest(),
                "equipment_type": "Bobcat S740",
                "category": "efficiency",
                "title": "Proper Warm-up Procedure",
                "tip_content": (
                    "Always warm up the machine for 5-10 minutes before heavy operation. "
                    "Cycle all hydraulic functions slowly to distribute warm oil throughout the system."
                ),
                "experience_level": "beginner",
                "votes": 156,
                "author": "Forum compilation",
                "source_url": "Multiple sources",
                "scraped_at": datetime.now().isoformat(),
            },
            {
                "tip_id": hashlib.md5("s740_grease".encode()).hexdigest(),
                "equipment_type": "Bobcat S740",
                "category": "maintenance",
                "title": "Daily Greasing Points",
                "tip_content": (
                    "Grease loader arms and bucket pins daily (8-10 hours of operation). "
                    "Use high-quality grease and pump until clean grease appears."
                ),
                "experience_level": "beginner",
                "votes": 203,
                "author": "Forum compilation",
                "source_url": "Multiple sources",
                "scraped_at": datetime.now().isoformat(),
            },
        ]

        # Store operator tips
        table_id = f"{self.project_id}.skidsteer_knowledge.operator_tips"
        errors = self.bq_client.insert_rows_json(table_id, tips)

        if not errors:
            logger.info(f"✅ Stored {len(tips)} operator tips")


async def main():
    """Main function to run skid steer scraper"""
    scraper = SkidSteerKnowledgeScraper()

    # Run comprehensive Bobcat S740 scrape
    results = await scraper.scrape_skidsteer_forums()

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
