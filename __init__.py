from aqt import mw
from aqt.utils import qconnect, tr, tooltip
from aqt.qt import QAction
from aqt import gui_hooks
from aqt import Collection
from aqt.operations import CollectionOp
from anki.collection import OpChangesWithCount
from .field_sort import reorder_cards
from .field_to_tag import add_tags
from .add_frequencies import populate_frequency

# Run in background logic
def success_tooltip(out) -> tooltip:
    try:
        return tooltip(tr.browsing_changed_new_position(count=out.count), parent=mw)
    except:
        pass

def run_in_background(func):
    def handle_nones(func_input):
        func_output = func(func_input)

        if func_output == None:
            return OpChangesWithCount(count=0)
        else:
            return func_output
    
    def run():
        operation = CollectionOp(parent=mw, op=handle_nones).success(success_tooltip)
        operation.run_in_background()

    return run

# Process cards on start
gui_hooks.main_window_did_init.append(run_in_background(reorder_cards))
gui_hooks.main_window_did_init.append(run_in_background(add_tags))

# Menu entries for each action
add_frequency_action = QAction("Add Missing Card Frequencies", mw)
reorder_cards_action = QAction("Reorder Cards", mw)
field_to_tags_action = QAction("Field to Tags", mw)

qconnect(add_frequency_action.triggered, run_in_background(populate_frequency))
qconnect(reorder_cards_action.triggered, run_in_background(reorder_cards))
qconnect(field_to_tags_action.triggered, run_in_background(add_tags))

mw.form.menuTools.addAction(add_frequency_action)
mw.form.menuTools.addAction(reorder_cards_action)
mw.form.menuTools.addAction(field_to_tags_action)
