#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_voice_studio info
PYTHONPATH=src python -m gbt_voice_studio check --payload '{}'
PYTHONPATH=src python -m gbt_voice_studio run   --payload '{}'
