## General Notes
* To disable one function off this addon remove the config group (for example remove "add_frequencies" if you don't want to add the option to prefill frequencies)
* Config won't work with default options, make sure to look at it and change things for your card types

## Auto Sort Cards based on Field
* `search_to_sort` - a search query for the cards to update, these will start at position 0
* `sort_field` - the note field to sort by
* `sort_reverse` - whether or not to sort in reverse order


**NOTE**: If your search query includes spaces in it you'll need to escape the quotes by adding a `\` before each `"`
* EXAMPLE - Search query `"deck:Japanese::Easy Learn" is:new` will become `"search_to_sort": "\"deck:Japanese::Easy Learn\" is:new"`

## Field to Tag
* `source_field` - sets what field for each note you want to use to set the tags as
* `prefixes` - strip text from the very start of a string pre-replacement
* `suffixes` - strip text from the very end of a string pre-replacement
* `replacements` - replacement patterns for the source field (to create the tag), if there is no replacement here then the tag will just be whatever was in the processed source field

**NOTE**: Spaces will be replaced with a special character (⠀) instead of being removed completely, feel free to use spaces anywhere here (they will be correctly handled)

## Add Frequencies to Old Cards
* `frequency_list_path` - path to a [Yomichan jpdb frequency list](https://github.com/MarvNC/jpdb-freq-list)
* `word_field` - the field on card with each word
* `reading_field` - the field on card with each words reading
* `frequency_field` - the field on card where frequencies should be inserted

**NOTE**: This won't do anything if the frequency list path isn't valid
