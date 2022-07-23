from aqt import mw
from aqt import Collection

config = mw.addonManager.getConfig(__name__)["field_sort"]

SEARCH_TO_SORT = config["search_to_sort"]
SORT_FIELD = config["sort_field"]
SORT_REVERSE = config["sort_reverse"]

def update_config():
    config = mw.addonManager.getConfig(__name__)["field_sort"]

    SEARCH_TO_SORT = config["search_to_sort"]
    SORT_FIELD = config["sort_field"]
    SORT_REVERSE = config["sort_reverse"]

def get_frequency(card):
    try:
        field = card.note()[SORT_FIELD]
        if field.strip() == "": return float("inf")
        else: return int(field)
    except:
        return float("inf")

# Adds tags via the source field
def reorder_cards(col: Collection) -> None:
    if "field_sort" not in mw.addonManager.getConfig(__name__):
        return
    
    update_config()

    # Get relevant cards
    card_ids = col.find_cards(SEARCH_TO_SORT, order="c.due asc")
    cards = [col.get_card(card_id) for card_id in card_ids]

    # Sort cards
    sorted_cards = sorted(cards, key=get_frequency, reverse=SORT_REVERSE)
    sorted_card_ids = [card.id for card in sorted_cards]

    # Reposition cards and apply changes
    if card_ids != sorted_card_ids:
        return col.sched.reposition_new_cards(
            card_ids=sorted_card_ids,
            starting_from=0, step_size=1,
            randomize=False, shift_existing=True
        )
