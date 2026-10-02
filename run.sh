#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [[ "${1:-}" == "--test" ]]; then
    PYTHONPATH=src python3 -m unittest discover -s tests -v
    exit 0
fi

PYTHONPATH=src python3 -m shell.main "$@"
