#!/usr/bin/env sh
set -eu

PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" scripts/validate-contract.py
