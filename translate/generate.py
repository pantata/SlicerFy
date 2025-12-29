#!/usr/bin/env python3
import polib  # pip install polib
import re
import sys
import os
from pathlib import Path

def load_translations(lang):
    # Try to find .po or .pot file
    candidates = [f"{lang}.po", f"{lang}.pot"]
    po_file = None
    for f in candidates:
        if os.path.exists(f):
            po_file = f
            break
    
    if not po_file:
        print(f"❌ Error: Translation file for '{lang}' not found. Checked: {', '.join(candidates)}")
        sys.exit(1)

    print(f"ℹ️  Loading translations from {po_file}...")
    try:
        po = polib.pofile(po_file, encoding='utf-8')
    except Exception as e:
        print(f"❌ Error parsing {po_file}: {e}")
        sys.exit(1)

    trans = {}
    for entry in po:
        # Clave = msgid (texto inglés original), valor = msgstr (traducción)
        if entry.msgstr.strip():
            # Desescapar para usar en reemplazo
            key = entry.msgid.replace('\\"', '"').replace('\\\\', '\\')
            val = entry.msgstr.replace('\\"', '"').replace('\\\\', '\\')
            trans[key] = val
    return trans

def replace_messages(input_cfg, trans_dict, output_cfg):
    try:
        with open(input_cfg, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Input config file '{input_cfg}' not found.")
        sys.exit(1)

    # Función de reemplazo: preserva variables ({port}, {VAR}, etc.)
    def replacer(match):
        prefix, orig_msg = match.group(1), match.group(2)
        # Busca traducción; si no existe, deja el original
        new_msg = trans_dict.get(orig_msg, orig_msg)
        return f'{prefix}="{new_msg}"'

    # Reemplaza MSG="..." y TITLE="..." (capturamos el prefijo para no tocar nada más)
    content = re.sub(
        r'(MSG|TITLE)\s*=\s*"([^"]*)"',
        replacer,
        content
    )

    # Guardar
    Path(output_cfg).parent.mkdir(parents=True, exist_ok=True)
    with open(output_cfg, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python generate.py <en_cfg> <lang>")
        print("Ej:  python generate.py slicerfy.cfg es")
        sys.exit(1)
    
    en_cfg = sys.argv[1] if len(sys.argv) > 1 else "../en/slicerfy.cfg"
    lang = sys.argv[2]
    trans = load_translations(lang)
    replace_messages(en_cfg, trans, f"../{lang}/slicerfy.cfg")
    print(f"✅ Generated {lang}/slicerfy.cfg with {len(trans)} translations applied")