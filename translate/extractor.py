import re
import sys
import pathlib

def print_help():
    help_text = (
        "Použití: python extractor.py <vstupní_cfg_soubor> <výstupní_soubor>\n"
        "Parametry:\n"
        "  <vstupní_cfg_soubor>  - cesta k vstupnímu CFG souboru\n"
        "  <výstupní_soubor>     - cesta k výstupnímu souboru, kam se zapíší nalezené zprávy\n"
        "Volitelné:\n"
        "  -h, --help            - zobrazí tuto nápovědu\n"
    )
    print(help_text)


if len(sys.argv) != 3:
    print_help()
    sys.exit(1)

if sys.argv[1] in ("-h", "--help"):
    print_help()
    sys.exit(0)

inp = sys.argv[1]
out = sys.argv[2]

cfg = pathlib.Path(inp).read_text(encoding="utf-8").splitlines()


pattern = re.compile(r'===(.*?)===')

found = []

for line in cfg:
    m = pattern.search(line)
    if m:
        txt = m.group(1).strip()
        if txt:
            found.append(txt)

with open(out, "w", encoding="utf-8") as f:
    for t in found:
        f.write(f"{t}  ;;;\n")