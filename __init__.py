from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import QAction
from aqt import gui_hooks

config = mw.addonManager.getConfig(__name__)

SEARCH_TO_SORT = config["search_to_sort"]
SORT_FIELD = config["sort_field"]
SORT_REVERSE = config["sort_reverse"]
SHIFT_EXISTING = config["shift_existing"]

# Adds tags via the source field
def reorder_cards() -> None:
    # Get relevant cards
    card_ids = mw.col.find_cards(SEARCH_TO_SORT, order=True)
    cards = [mw.col.get_card(card_id) for card_id in card_ids]

    # Sort cards
    sorted_cards = sorted(cards, key=lambda card: card.note()[SORT_FIELD], reverse=SORT_REVERSE)
    sorted_card_ids = [card.id for card in sorted_cards]

    # Reposition cards
    mw.col.sched.reposition_new_cards(sorted_card_ids, starting_from=0, step_size=1, randomize=0, shift_existing=SHIFT_EXISTING)

    # Apply changes
    mw.col.update_cards(sorted_cards)

# Run on sync
gui_hooks.sync_will_start.append(reorder_cards)
