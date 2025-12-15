import re
import sys
import pathlib
from typing import Set

def print_help():
    """Vytiskne nápovědu k použití skriptu."""
    help_text = (
        "Použití: python extractor.py <vstupní_cfg_soubor> <výstupní_soubor>\n"
        "Parametry:\n"
        "  <vstupní_cfg_soubor>  - cesta k vstupnímu CFG souboru\n"
        "  <výstupní_soubor>     - cesta k výstupnímu souboru, kam se zapíší nalezené zprávy\n"
        "Volitelné:\n"
        "  -h, --help            - zobrazí tuto nápovědu\n"
    )
    print(help_text)

def get_existing_messages(output_path: pathlib.Path) -> Set[str]:
    """
    Načte existující zprávy z výstupního souboru a vrátí je jako množinu.
    Očekává formát 'puvodni_retezec ;;; preklad\n'.

    :param output_path: Cesta k výstupnímu souboru.
    :return: Množina existujících zpráv.
    """
    existing_messages = set()
    if output_path.exists():
        try:
            content = output_path.read_text(encoding="utf-8").splitlines()
            for line in content:
                parts = line.split(" ;;; ")
                if parts and parts[0].strip():
                    existing_messages.add(parts[0].strip())
        except Exception as e:
            print(f"Varování: Nepodařilo se načíst existující zprávy ze souboru '{output_path}': {e}", file=sys.stderr)
            # Pokračujeme s prázdnou množinou, abychom nenarušili běh

    return existing_messages

# --- Kontrola a zpracování argumentů ---

# Kontrola minimálního počtu argumentů a zpracování nápovědy
if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print_help()
    sys.exit(0)

if len(sys.argv) != 3:
    print("Chyba: Očekávají se 2 poziční argumenty: <vstupní_cfg_soubor> <výstupní_soubor>", file=sys.stderr)
    print_help()
    sys.exit(1)


inp_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])

# Kontrola existence vstupního souboru
if not inp_path.is_file():
    print(f"Chyba: Vstupní soubor '{inp_path}' neexistuje nebo není soubor.", file=sys.stderr)
    sys.exit(1)


# --- Načtení existujících zpráv z výstupního souboru ---

existing_messages = get_existing_messages(out_path)

# --- Načtení a zpracování vstupního souboru ---

try:
    cfg = inp_path.read_text(encoding="utf-8").splitlines()
except Exception as e:
    print(f"Chyba při čtení vstupního souboru '{inp_path}': {e}", file=sys.stderr)
    sys.exit(1)


pattern = re.compile(r'===(.*?)===')
newly_found_unique = set()

# Hledání nových zpráv ve vstupním souboru
for line in cfg:
    matches = pattern.findall(line)
    for match in matches:
        txt = match.strip()
        # Zpráva musí existovat A NESMÍ být již ve výstupním souboru
        if txt and txt not in existing_messages:
            newly_found_unique.add(txt)


# --- Zápis nových zpráv ---

# Otevření souboru v režimu připojení (append, 'a'), 
# aby se zachoval stávající obsah a přidaly se jen nové řádky.
if newly_found_unique:
    try:
        with out_path.open("a", encoding="utf-8") as f:
            for t in newly_found_unique:
                f.write(f"{t} ;;; {t}\n")
        print(f"Úspěšně přidáno {len(newly_found_unique)} unikátních zpráv do '{out_path}'.")
    except Exception as e:
        print(f"Chyba při zápisu do výstupního souboru '{out_path}': {e}", file=sys.stderr)
        sys.exit(1)
else:
    print(f"Ve vstupním souboru nebyly nalezeny žádné nové unikátní zprávy pro '{out_path}'.")