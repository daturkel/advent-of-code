We have a word search with two possible things to search for.

1. To find XMAS in any direction, we scan the puzzle looking for X. When we find X, we search in every direction to see if it's XMAS and if it is we add it to our count. In particular, we move 1 in each direction progressively checking to see if it's the next letter in the word and stop if it's not. I also tried checking the entire word in one go (rather than stopping early if the substring was wrong) but this actually turned out slower due to all the extra array accesses.
2. To find
M.S
.A.
M.S
(MAS or SAM crossed in an X)
we scan the puzzle looking for S or M and when we find it, we check to see if it's in this arrangement.