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
        {"name": "Part of Speech"},
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
            "qfmt": "{{Greek}}<br>{{Part of Speech}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{English}}',
        },
        {
            "name": "Card 2",
            "qfmt": "{{English}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Greek}}',
        },
    ],
)
secs = {
    'Ἐπίθετα': "Ἐπίθετον",
    'Ἐπιφωνήματα': "Ἐπιφωνήμα",
    'Ἐπιρρήματα': "Ἐπιρρήμα",
    'Φράσεις': "Φράσις",
    'Ἀριθμοί': "Ἀριθμός",
    'Ὀνόματα': "Ὀνόμα",
    'Ἐκφράσεις': "Ἐκφράσις",
    'Ἀντωνυμίαι': "Ἀντωνυμία",
    'Ῥήματα': "Ῥήμα",
    'Ἄρθρον': "Ἄρθρον",
    'Προθέσεις': "Προθέσις",
    'Σύνδεσμοι': "Σύνδεσμος",
    'Μόρια': "Μόριον"
}
for file in Path.cwd().glob("json/*.json"):
    ch = file.stem.split(' ')[1]
    data = json.loads(file.read_text(encoding="utf-8"))

    for section in data["sections"]:
        if section["section"].lower() == "κύρια ὀνόματα":
            continue
        pos = secs[section["section"]].lower()
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
            print(f"Adding {greek} {gloss} {pos}")
            deck.add_note(genanki.Note(model=model, fields=[greek, gloss, pos], tags=[f"{ch}"]))

genanki.Package(deck).write_to_file("output.apkg")
