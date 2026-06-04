#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/etl"

export PYTHONPATH="${ROOT}:${PYTHONPATH:-}"
cd "$ROOT"
python -m etl.jobs.run_pipeline
