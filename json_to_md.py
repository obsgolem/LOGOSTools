import json
from pathlib import Path
import unicodedata

"""
Converts the JSON documents to markdown for easier human consumption
"""

out_dir = Path.cwd() / "generated_markdown"
out_dir.mkdir(exist_ok=True)

for file in Path.cwd().glob("json/*.json"):
    with file.open() as f:
        data = json.load(f)
    with (out_dir / f"{file.stem} {data['chapter_name']}.md").open("w") as f:
        print(f"Pg. {data['word_list_page_number']}  ", file=f)
        print(
            f"Ex. {data['exercise_page_range'][0]}-{data['exercise_page_range'][1]}  ",
            file=f,
        )
        for section in data["sections"]:
            print(f"# {unicodedata.normalize('NFC', section['section'])}  ", file=f)
            for word in section["words"]:
                print(f"{unicodedata.normalize('NFC', word['book_entry'])}  ", file=f)
