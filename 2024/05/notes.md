Part 1 is straightforwrd: build up a list of "followers", i.e. {"a": ["b","c"]} means b and c must follow a. Then iterate through every page list backwards, making sure the pages added to the end are followers of the next page to insert at the beginning.

For part two, we need to re-sort the incorrectly sorted ones. I implemented insertion sort.