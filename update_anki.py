import sys
import unicodedata
import json
import csv
from pathlib import Path

update_data = dict()

for file in Path.cwd().glob("json/*.json"):
    ch = file.stem.split(' ')[1]
    data = json.loads(file.read_text(encoding="utf-8"))

    for section in data["sections"]:
        if section["section"].lower() == "κύρια ὀνόματα":
            continue
        for word in section["words"]:
            greek = word["macronized"] if "macronized" in word else word["book_entry"]
            greek = greek.replace("_","")
            if greek[0].upper() == greek[0]:
                # skip name-ish stuff
                continue
            if "gloss" not in word:
                continue
            gloss = word["gloss"]
            greek = unicodedata.normalize("NFC", greek)

            update_data.setdefault(greek, dict())
            update_data[greek] = update_data[greek] | { ch : gloss }

out = ""
with open(sys.argv[1], newline='', encoding="utf-8") as csvfile:
    for line in csvfile:
        edit = line.split("\t")
        try:
            if len(edit) == 6:
                edit[3] = update_data[edit[2]][edit[5].strip()]
        except KeyError:
            pass
        out += '\t'.join(edit)

with open(sys.argv[1], mode="w", encoding="utf-8") as csvfile:
    csvfile.write(out)