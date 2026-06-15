#!/usr/bin/env bash
set -euo pipefail
DMC="${DMC:-dmc}"
root="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$root/verify/verify_port.py" --mode floats \
  --ref python3 "$root/lion_step.py" \
  --dmc $DMC run "$root/lion_step.dmc"
