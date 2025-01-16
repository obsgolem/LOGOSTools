import genanki
import unicodedata
import json
from pathlib import Path

deck = genanki.Deck(2069123839, "ΛΟΓΟΣ vocab")

model = genanki.Model(
    2015670040,
    "ΛΟΓΟΣ",
    fields=[
        {"name": "Greek"},
        {"name": "English"},
    ],
    css=""".card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}""",
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Greek}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{English}}',
        },
        {
            "name": "Card 2",
            "qfmt": "{{English}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Greek}}',
        },
    ],
)

for file in Path.cwd().glob("json/*.json"):
    data = json.loads(file.read_text(encoding="utf-8"))

    for section in data["sections"]:
        for word in section["words"]:
            word = word["macronized"] if "macronized" in word else word["book_entry"]
            if "gloss" not in word:
                continue
            gloss = word.gloss
            word = unicodedata.normalize("NFC", word)
            deck.add_note(genanki.Note(model=model, fields=[word, gloss]))

genanki.Package(deck).write_to_file("output.apkg")
