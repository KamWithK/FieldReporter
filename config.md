## Config Options
* `search_to_sort` - a search query for the cards to update, these will start at position 0
* `sort_field` - the note field to sort by
* `sort_reverse` - whether or not to sort in reverse order
* `shift_existing` - whether or not to shift existing

## NOTES:
* **Anki must *restart* before config changes take place**
* If your search query includes spaces in it you'll need to escape the quotes by adding a `\` before each `"`:
    * EXAMPLE - Search query `"deck:Japanese::Easy Learn" is:new` will become `"search_to_sort": "\"deck:Japanese::Easy Learn\" is:new"`