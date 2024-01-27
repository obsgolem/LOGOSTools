from pathlib import Path
import re
import unicodedata
import json

"""
Converts the original markdown files into json files so we can add metadata to them
"""

chap_extractor = re.compile(r"Ch (\d*) (.*)")
page_extractor = re.compile(r"Pg\.? (.*)")
ex_extractor = re.compile(r"Ex. (.*)-(.*)")
header_extractor = re.compile(r"# (.*)")

for file in (Path.cwd() / "original_markdown").glob("*.md"):
    (number, name) = chap_extractor.match(file.stem).group(1, 2)

    name = unicodedata.normalize("NFKD", name)
    with file.open() as f:
        page = next(f)
        word_list_page = page_extractor.match(page).group(1)
        ex_pages = ex_extractor.match(next(f)).group(1, 2)
        sections = []
        for line in f:
            line = unicodedata.normalize("NFKD", line).strip()
            header = header_extractor.match(line)
            if header:
                current_sect = header.group(1)
                sections.append({"section": current_sect, "words": []})
            else:
                sections[-1]["words"].append({"book_entry": line})
        final_object = {
            "chapter_name": name,
            "word_list_page_number": int(word_list_page),
            "exercise_page_range": [int(ex_pages[0]), int(ex_pages[1])],
            "sections": sections,
        }
        with (Path.cwd() / f"json/Ch {number}.json").open("w") as out:
            json.dump(final_object, out, indent=2, ensure_ascii=False)
