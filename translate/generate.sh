#!/bin/bash
set -e

for lang in es de cs ru; do
  echo "   → $lang"
  python3 generate.py ../en/slicerfy.cfg $lang
done