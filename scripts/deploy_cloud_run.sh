#!/usr/bin/env bash
set -euo pipefail
gcloud run deploy bobs-brain --region "${LOCATION}" --project "${PROJECT_ID}" --source .
