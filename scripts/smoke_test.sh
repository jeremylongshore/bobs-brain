#!/usr/bin/env bash
set -euo pipefail
curl -sf http://127.0.0.1:${PORT:-8080}/_health >/dev/null
curl -sf http://127.0.0.1:${PORT:-8080}/ >/dev/null
echo "smoke: ok"
