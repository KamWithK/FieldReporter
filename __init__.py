from aqt import mw
from aqt.utils import showInfo, qconnect, tr, tooltip
from aqt.qt import QAction
from aqt import gui_hooks
from aqt import Collection
from aqt.operations import CollectionOp
from anki.collection import OpChangesWithCount

config = mw.addonManager.getConfig(__name__)

SEARCH_TO_SORT = config["search_to_sort"]
SORT_FIELD = config["sort_field"]
SORT_REVERSE = config["sort_reverse"]
SHIFT_EXISTING = config["shift_existing"]

def get_frequency(card):
    try:
        field = card.note()[SORT_FIELD]
        if field.strip() == "": return float("inf")
        else: return int(field)
    except:
        return float("inf")

# Adds tags via the source field
def reorder_cards(col: Collection) -> None:
    # Get relevant cards
    card_ids = mw.col.find_cards(SEARCH_TO_SORT, order="c.due asc")
    cards = [mw.col.get_card(card_id) for card_id in card_ids]

    # Sort cards
    sorted_cards = sorted(cards, key=get_frequency, reverse=SORT_REVERSE)
    sorted_card_ids = [card.id for card in sorted_cards]

    # Avoid making unnecessary changes
    if card_ids == sorted_card_ids:
        return OpChangesWithCount(count=0)
    
    # Reposition cards and apply changes
    return mw.col.sched.reposition_new_cards(
        card_ids=sorted_card_ids,
        starting_from=0, step_size=1,
        randomize=False, shift_existing=SHIFT_EXISTING
    )

def run_in_background():
    operation = CollectionOp(parent=mw, op=reorder_cards).success(
        lambda out: tooltip(
            tr.browsing_changed_new_position(count=out.count), parent=mw if out.count != 0 else None
        )
    )
    operation.run_in_background()

# Run on sync
gui_hooks.main_window_did_init.append(run_in_background)
