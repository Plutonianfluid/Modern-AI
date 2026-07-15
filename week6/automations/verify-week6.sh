#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHONPATH=. pytest -q backend/tests "$@"
ruff check backend
black --check backend
