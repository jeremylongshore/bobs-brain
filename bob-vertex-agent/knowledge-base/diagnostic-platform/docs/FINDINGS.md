# DIAGPRO Vertex→PDF Remediation Findings

## Root Causes
- Legacy Vertex workflow lacked a formal JSON schema, permitting unbounded fields and overlong payloads.
- Prompt instructions did not enforce confidence uplift or readiness verdict rules, leading to inconsistent downstream rendering.
- Guardrails for output length, pagination, and confidence thresholds were absent, causing the 33-page regression and repeated manual triage.

## Schema & Prompt Updates
- Authored `src/schema/diagpro.report.schema.json` to lock field names, enforce uppercase enums, and require confidence/readiness metadata.
- Added system prompt `src/prompts/vertex.system.txt` with strict JSON-only response rules, safety guidance, and automatic uplift expectations when confidence < threshold.
- Added templated user prompt `src/prompts/vertex.user.template.txt` so ingestion passes structured submission, code, and note payloads with configurable confidence threshold (default 85%).
- Documented render map in `docs/RENDER.MAP.md` aligning schema elements to PDF sections, including confidence block and readiness footer.

## Test Results (Mocks A–H)
| Case | Pages (≈3000 chars ea) | Confidence | Verdict |
| --- | --- | --- | --- |
| A | 0.4 | 92 | READY |
| B | 0.5 | 72 | FOLLOW_UP |
| C | 0.4 | 88 | FOLLOW_UP |
| D | 0.4 | 83 | FOLLOW_UP |
| E | 0.6 | 65 | NOT_READY |
| F | 0.5 | 80 | FOLLOW_UP |
| G | 0.4 | 55 | FOLLOW_UP |
| H | 0.6 | 70 | FOLLOW_UP |

All guard scripts (`validate_schema.sh`, `length_guard.sh`, `page_estimator.py`, `confidence_guard.sh`, `readiness_guard.sh`) executed successfully against A–H outputs.

## 33-Page Regression
- Input fixture: `tests/regress/oversize.json` (simulated from historical 33-page case).
- Previous behavior: 33-page PDF with repeated findings and runaway pagination.
- Current result: `tests/outputs/oversize.json` ≈0.3 pages, CONFIDENCE 60, verdict FOLLOW_UP.
- Guards: schema, length, pagination, confidence, readiness all PASS under stress allowances.
