#!/usr/bin/env python3
"""
Circle of Life - Evidence-driven learning loop
No external scrapers. Inputs from /learn API and internal signals.
"""

import hashlib
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple

# Configuration from environment
CONFIDENCE_MIN = float(os.getenv("BB_CONFIDENCE_MIN", "0.6"))
BATCH_SIZE = int(os.getenv("BB_COL_BATCH", "50"))
COOLDOWN_SEC = int(os.getenv("BB_COL_COOLDOWN", "60"))


def content_hash(obj: Any) -> str:
    """Generate deterministic hash for deduplication"""
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


class CircleOfLife:
    """
    Evidence-driven learning loop:
      ingest(events) -> analyze(patterns) -> llm insights -> persist -> apply
    No external scrapers. Inputs come from API (/learn) or internal signals.
    """

    def __init__(self, neo4j_driver=None, bq_client=None, llm_call=None, logger=None):
        self.driver = neo4j_driver
        self.bq = bq_client
        self.llm_call = llm_call
        self.log = logger or logging.getLogger("circle_of_life")
        self._last_run = 0
        self._processed_hashes = set()

    def ready(self) -> bool:
        """Check if enough time has passed since last run (cooldown)"""
        return (time.time() - self._last_run) >= COOLDOWN_SEC

    def ingest(self, events: List[Dict]) -> List[Dict]:
        """
        Deduplicate and batch events for processing
        Returns list of unique events up to BATCH_SIZE
        """
        batch = []
        for ev in events:
            h = content_hash(ev)
            if h in self._processed_hashes:
                continue
            self._processed_hashes.add(h)
            batch.append(ev)
            if len(batch) >= BATCH_SIZE:
                break

        # Cleanup old hashes to prevent memory growth
        if len(self._processed_hashes) > BATCH_SIZE * 10:
            self._processed_hashes.clear()

        return batch

    def analyze(self, batch: List[Dict]) -> Dict:
        """
        Analyze batch of events for patterns
        Simple grouping by type - can be enhanced with ML
        """
        by_type = {}
        by_user = {}
        total_events = len(batch)

        for ev in batch:
            event_type = ev.get("type", "unknown")
            user_id = ev.get("user_id", "anonymous")

            by_type.setdefault(event_type, []).append(ev)
            by_user.setdefault(user_id, []).append(ev)

        return {
            "total_events": total_events,
            "event_types": {k: len(v) for k, v in by_type.items()},
            "users": {k: len(v) for k, v in by_user.items()},
            "sample_events": batch[:3],
            "timestamp": time.time(),
        }

    def generate_insights(self, analysis: Dict) -> List[Dict]:
        """
        Generate insights from analysis using LLM with retry/backoff
        """
        if not self.llm_call:
            # Return mock insight if no LLM configured
            return [
                {
                    "pattern": "mock_pattern",
                    "confidence": 0.9,
                    "description": "Mock insight for testing",
                    "meta": analysis,
                }
            ]

        payload = {
            "task": "extract learning patterns and action items",
            "analysis": analysis,
            "min_confidence": CONFIDENCE_MIN,
        }

        # Retry with exponential backoff
        for attempt in range(3):
            try:
                result = self.llm_call(payload)
                if isinstance(result, list):
                    return result
                else:
                    return [result] if result else []
            except Exception as e:
                self.log.warning(f"LLM call failed attempt {attempt + 1}: {e}")
                if attempt < 2:  # Don't sleep on final attempt
                    time.sleep(2**attempt)

        return []

    def persist(self, insights: List[Dict]) -> Tuple[int, int]:
        """
        Persist high-confidence insights to Neo4j and BigQuery
        Returns (neo4j_writes, bigquery_writes)
        """
        wrote_neo4j = 0
        wrote_bq = 0

        high_confidence_insights = [ins for ins in insights if float(ins.get("confidence", 0)) >= CONFIDENCE_MIN]

        # Persist to Neo4j
        if self.driver and high_confidence_insights:
            try:
                with self.driver.session() as session:
                    for insight in high_confidence_insights:
                        session.run(
                            """
                            MERGE (i:Insight {id: $id})
                            SET i.pattern = $pattern,
                                i.confidence = $confidence,
                                i.description = $description,
                                i.timestamp = timestamp(),
                                i.updated_at = datetime()
                            """,
                            id=content_hash(insight),
                            pattern=insight.get("pattern", ""),
                            confidence=float(insight.get("confidence", 0.0)),
                            description=insight.get("description", ""),
                        )
                        wrote_neo4j += 1
            except Exception as e:
                self.log.error(f"Neo4j persist failed: {e}")

        # Persist to BigQuery (simplified - would need table schema in production)
        if self.bq and high_confidence_insights:
            wrote_bq = len(high_confidence_insights)
            # Stub: In production, would insert into specific table
            self.log.info(f"Would persist {wrote_bq} insights to BigQuery")

        return wrote_neo4j, wrote_bq

    def apply(self, insights: List[Dict]) -> int:
        """
        Apply insights to improve future responses
        Returns number of insights applied
        """
        applied = 0
        for insight in insights:
            if float(insight.get("confidence", 0)) >= CONFIDENCE_MIN:
                # Hook: update indices, caches, or prompt-memory
                # In production: update response templates, user preferences, etc.
                applied += 1
                self.log.info(f"Applied insight: {insight.get('pattern', 'unknown')}")

        return applied

    def run_once(self, events: List[Dict]) -> Dict:
        """
        Main Circle of Life learning cycle
        Returns metrics about the run
        """
        if not self.ready():
            return {"ran": False, "reason": "cooldown", "next_run_in": COOLDOWN_SEC - (time.time() - self._last_run)}

        start_time = time.time()

        # Process events through the learning pipeline
        batch = self.ingest(events)
        if not batch:
            return {"ran": False, "reason": "no_new_events"}

        analysis = self.analyze(batch)
        insights = self.generate_insights(analysis)
        neo4j_writes, bq_writes = self.persist(insights)
        applied = self.apply(insights)

        self._last_run = time.time()
        duration = self._last_run - start_time

        return {
            "ran": True,
            "duration_seconds": round(duration, 3),
            "batch_size": len(batch),
            "insights_generated": len(insights),
            "high_confidence_insights": len([i for i in insights if float(i.get("confidence", 0)) >= CONFIDENCE_MIN]),
            "neo4j_writes": neo4j_writes,
            "bigquery_writes": bq_writes,
            "applied": applied,
            "analysis": analysis,
            "timestamp": self._last_run,
        }


# Global instance factory
_circle_of_life_instance = None


def get_circle_of_life(**kwargs) -> CircleOfLife:
    """Get or create global Circle of Life instance"""
    global _circle_of_life_instance
    if _circle_of_life_instance is None:
        _circle_of_life_instance = CircleOfLife(**kwargs)
    return _circle_of_life_instance
