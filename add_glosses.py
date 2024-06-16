from pathlib import Path
import json
import re
import unicodedata

"""
Takes the output of scrape.py and uses it to add initial glosses to the json files.
"""

splitter = re.compile(r"[^,\s;]*")
for file in (Path.cwd() / "json").glob("*.json"):
    print(file)
    contents = json.loads(file.read_text(encoding="utf-8"))

    defs = json.loads(
        ((Path.cwd() / "logeion") / file.name).read_text(encoding="utf-8")
    )

    for section in contents["sections"]:
        for word in section["words"]:
            clean = next(splitter.finditer(word["book_entry"])).group(0)
            clean = unicodedata.normalize("NFKC", clean)

            try:
                cleandef: str = defs[clean]["detail"]["shortdef"][0]
                for i, c in enumerate(cleandef):
                    if not c.isascii() or c.isspace() or c == ",":
                        continue
                    else:
                        cleandef = cleandef[i:]
                        break
                word["gloss"] = cleandef
            except IndexError:
                del word["gloss"]
                continue

    with file.open("wb") as out:
        out.write(json.dumps(contents, indent=2, ensure_ascii=False).encode("utf-8"))
