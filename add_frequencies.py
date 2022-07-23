import os
import json

from aqt import mw
from aqt import Collection

config = mw.addonManager.getConfig(__name__)["add_frequencies"]

FREQUENCY_LIST_PATH = config["frequency_list_path"]
WORD_FIELD = config["word_field"]
READING_FIELD = config["reading_field"]
FREQUENCY_FIELD = config["frequency_field"]

def update_config():
    config = mw.addonManager.getConfig(__name__)["add_frequencies"]

    FREQUENCY_LIST_PATH = config["frequency_list_path"]
    WORD_FIELD = config["word_field"]
    READING_FIELD = config["reading_field"]
    FREQUENCY_FIELD = config["frequency_field"]

# Example entry from JPDB frequency list
if os.path.exists(FREQUENCY_LIST_PATH):
    with open(FREQUENCY_LIST_PATH, encoding="utf-8-sig") as file:
        FREQUENCY_DATA = json.load(file)
else:
    FREQUENCY_DATA = None

def is_same_kana(word: str, sample: str) -> bool:
    return word == sample

def is_same_word(word: str, word_reading: str, sample: str, sample_reading: str) -> bool:
    return word == sample and word_reading == sample_reading

def populate_frequency(col: Collection) -> None:
    if "add_frequencies" not in mw.addonManager.getConfig(__name__) or FREQUENCY_DATA == None:
        return
    
    update_config()
    
    # Get tags without frequency
    notes = [col.get_note(note_id) for note_id in col.find_notes(f"-{FREQUENCY_FIELD}:_*")]

    for index, note in enumerate(notes):
        if WORD_FIELD not in note or READING_FIELD not in note:
            continue
        
        word, reading = note[WORD_FIELD], note[READING_FIELD]

        # Loop through and get entry with identical word and reading, use `value` field
        for sample_word, _, sample_readings in FREQUENCY_DATA:
            if "reading" in sample_readings and is_same_word(word, reading, sample_word, sample_readings["reading"]):
                note[FREQUENCY_FIELD] = str(sample_readings["frequency"]["value"])
                break
            elif "reading" not in sample_readings and is_same_kana(word, sample_word):
                note[FREQUENCY_FIELD] = str(sample_readings["value"])
                break

        # Update progress bar
        mw.taskman.run_on_main(
            lambda: mw.progress.update(
                label=f"{word} ({index}/{len(notes)})",
                value=index,
                max=len(notes)
            )
        )

    # Apply changes
    return col.update_notes(notes)
