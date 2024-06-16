import httpx
from pathlib import Path
import json
import re
import unicodedata

"""
Loops over all the words in the word list and pulls the data from Logeion for it. This is a best effort script.
"""

splitter = re.compile(r"[^,\s;]*")
for file in (Path.cwd() / "json").glob("*.json"):
    print(file)
    contents = json.loads(file.read_text(encoding="utf-8"))
    out = {}
    for section in contents["sections"]:
        for word in section["words"]:
            clean = next(splitter.finditer(word["book_entry"])).group(0)
            clean = unicodedata.normalize("NFKC", clean)

            try:
                result = httpx.get(
                    "https://api-v2.logeion.org/detail",
                    params={
                        "key": "AIzaSyCT5aVzk3Yx-m8FH8rmTpEgfVyVA3pYbqg",
                        "type": "normal",
                        "w": clean,
                    },
                    headers={"Referer": "https://logeion.uchicago.edu/"},
                ).json()

                out[clean] = result

            except:
                continue

    with (file.parent.parent / "logeion" / file.name).open("wb") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False).encode("utf-8"))
