#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

./utils/generate-env.sh
docker compose build
