#!/bin/bash
set -e

python3 extract.py ../en/slicerfy.cfg

for lang in es fr de it pt cs ru tr; do
  echo "   → $lang"
  msgmerge --no-fuzzy-matching --backup=none -U $lang.po base.pot
  msgattrib --no-obsolete $lang.po -o $lang.po
done

echo "✅ Done. Now translate the empty entries in Poedit."
echo "💡 Then run: generate.sh"