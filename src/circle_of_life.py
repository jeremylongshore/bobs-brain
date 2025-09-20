import hashlib
import json
import logging
import os
import time
from typing import Any, Dict, List, Tuple

CONFIDENCE_MIN = float(os.getenv("BB_CONFIDENCE_MIN", "0.6"))
BATCH_SIZE = int(os.getenv("BB_COL_BATCH", "50"))
COOLDOWN_SEC = int(os.getenv("BB_COL_COOLDOWN", "60"))


def content_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


class CircleOfLife:
    """ingest -> analyze -> llm insights -> persist -> apply"""

    def __init__(self, neo4j_driver=None, bq_client=None, llm_call=None, logger=None):
        self.driver = neo4j_driver
        self.bq = bq_client
        self.llm_call = llm_call
        self.log = logger or logging.getLogger("circle")
        self._last_run = 0

    def ready(self) -> bool:
        return (time.time() - self._last_run) >= COOLDOWN_SEC

    def ingest(self, events: List[Dict]) -> List[Dict]:
        seen, out = set(), []
        for ev in events:
            h = content_hash(ev)
            if h in seen:
                continue
            seen.add(h)
            out.append(ev)
            if len(out) >= BATCH_SIZE:
                break
        return out

    def analyze(self, batch: List[Dict]) -> Dict:
        by_type = {}
        for ev in batch:
            by_type.setdefault(ev.get("type", "event"), 0)
            by_type[ev.get("type", "event")] += 1
        return {"counts": by_type, "sample": batch[:3]}

    def generate_insights(self, analysis: Dict) -> List[Dict]:
        if not self.llm_call:
            return []
        prompt = (
            "Return ONLY JSON list of objects: "
            '[{"pattern": str, "action": str, "confidence": float}] based on: '
            f"{json.dumps(analysis)}"
        )
        for i in range(3):
            try:
                import json as _json

                txt = self.llm_call(prompt)
                data = _json.loads(txt)
                return data if isinstance(data, list) else []
            except Exception as e:
                self.log.warning("llm fail %s: %s", i + 1, e)
                time.sleep(2**i)
        return []

    def persist(self, insights: List[Dict]) -> Tuple[int, int]:
        g = bq = 0
        if self.driver:
            from neo4j import GraphDatabase  # noqa

            with self.driver.session() as s:
                for ins in insights:
                    if float(ins.get("confidence", 0)) < CONFIDENCE_MIN:
                        continue
                    s.run(
                        "MERGE (i:Insight {id:$id}) "
                        "SET i.pattern=$p, i.action=$a, i.confidence=$c, i.ts=timestamp()",
                        id=content_hash(ins),
                        p=ins.get("pattern"),
                        a=ins.get("action"),
                        c=float(ins.get("confidence", 0.0)),
                    )
                    g += 1
        # bq stub: count items that pass threshold
        bq = len([i for i in insights if float(i.get("confidence", 0)) >= CONFIDENCE_MIN]) if self.bq else 0
        return g, bq

    def apply(self, insights: List[Dict]) -> int:
        return len([i for i in insights if float(i.get("confidence", 0)) >= CONFIDENCE_MIN])

    def run_once(self, events: List[Dict]) -> Dict:
        if not self.ready():
            return {"ran": False, "reason": "cooldown"}
        batch = self.ingest(events)
        analysis = self.analyze(batch)
        insights = self.generate_insights(analysis)
        g, bq = self.persist(insights)
        applied = self.apply(insights)
        self._last_run = time.time()
        return {
            "ran": True,
            "batch": len(batch),
            "insights": len(insights),
            "persist_graph": g,
            "persist_bq": bq,
            "applied": applied,
        }
