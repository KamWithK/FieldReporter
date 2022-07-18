from aqt import mw
from aqt import Collection
from anki.collection import OpChangesWithCount

config = mw.addonManager.getConfig(__name__)["field_to_tag"]

SOURCE_FIELD = config["source_field"]
PREFIXES = config["prefixes"]
SUFFIXES = config["suffixes"]
REPLACEMENTS = config["replacements"]

def update_config():
    config = mw.addonManager.getConfig(__name__)["field_to_tag"]

    SOURCE_FIELD = config["source_field"]
    PREFIXES = config["prefixes"]
    SUFFIXES = config["suffixes"]
    REPLACEMENTS = config["replacements"]

# Removes the first found suffix
def remove_prefixes(field: str) -> str:
    for prefix in PREFIXES:
        if field.startswith(prefix):
            return field[len(prefix):]
    
    return field

# Removes the first found suffix
def remove_suffixes(field: str) -> str:
    for suffix in SUFFIXES:
        if field.endswith(suffix):
            return field[:-len(suffix)]
    
    return field

# Swaps based on the first found replacement
def apply_replacements(original: str) -> str:
    stripped = remove_suffixes(remove_prefixes(original))
    if stripped in REPLACEMENTS:
        return REPLACEMENTS[stripped]
    elif original in REPLACEMENTS:
        return REPLACEMENTS[original]
    else:
        return stripped

# Adds tags via the source field
def add_tags(col: Collection) -> None:
    update_config()

    # Get untagged notes with the source field not-empty
    notes = [col.get_note(note_id) for note_id in col.find_notes(f"tag:none {SOURCE_FIELD}:_*")]

    for note in notes:
        # Attempt to use replacements
        tag = apply_replacements(note[SOURCE_FIELD]).replace(" ", "⠀")

        # Add tags
        note.add_tag(tag)

    # Apply changes
    return col.update_notes(notes)
