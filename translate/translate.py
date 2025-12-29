# (C) 2025 ghzserg https://github.com/ghzserg/zmod/
import csv
import os
import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) not in [2, 3]:
        print("Použití: python translate.py <soubor_překladu.txt> [vstupní_cfg_soubor]")
        print("Pokud [vstupní_cfg_soubor] není zadán, zpracují se všechny .cfg soubory v nadřazeném adresáři.")
        return

    translate_file = sys.argv[1]
    lang_dir = os.path.splitext(translate_file)[0]

    output_dir = Path(f"../{lang_dir}")
    output_dir.mkdir(exist_ok=True)

    translations = {}
    with open(translate_file, 'r', encoding='utf-8') as f:
        for line in f:
            if ';;;' in line:
                original, translated = line.split(';;;', 1)
                translations[original.strip()] = translated.strip()

    pattern = re.compile(r'(===)(.*?)(===)')

    def translate_line(line):
        def replace_match(match):
            original_text = match.group(2).strip()
            translated_text = translations.get(original_text, original_text)
            return f"{translated_text}"

        return pattern.sub(replace_match, line)

    cfg_files_to_process = []
    if len(sys.argv) == 3:
        cfg_path = Path(sys.argv[2])
        if not cfg_path.is_file():
            print(f"Chyba: Vstupní soubor '{cfg_path}' neexistuje nebo není soubor.")
            return
        cfg_files_to_process.append(cfg_path)
    else:
        cfg_files_to_process = list(Path('../').glob('*.cfg'))

    for cfg_file in cfg_files_to_process:
        with open(cfg_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()

        translated_lines = [translate_line(line) for line in lines]

        output_path = output_dir / cfg_file.name
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(translated_lines)

    print(f"Přeloženo souborů: {len(cfg_files_to_process)} do adresáře '{output_dir}'")

if __name__ == "__main__":
    main()