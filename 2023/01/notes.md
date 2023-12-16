This is a much spicier Day 1 than previous years.

I solved both parts with regex but part 1 would be fairly easy to do with a plain old loop.

Part 2 is where things become interesting, though not always for great reason.

First off, having to create a dict of {"one": 1, "two": 2, ...} is a surprisingly ugly thing to do on Day 1.
I feel like the first few days should be solveable more or less in a couple of lines, and that adds some inelegant length to the solution.

But the really painful thing was having to deal with overlapping strings. From the test input, we have:
`eightwothree`, which has a first digit of 8 and a last digit of 3, so becomes 83
However, we need to parse it as 8, 2, 3, even though "eight" and "two" overlap, because in the *real* input, this sometimes matters (i.e. the overlap can impact the last digit).
IMO, this subtlety should be evident in the test input: I would've expected that not handling this case should make my test input wrong. Instead, my test solution worked but my real input solution didn't and I had to manually double check how I was parsing each line to find what was going wrong. Also, the second set of test inputs had a line with no digits in it, which breaks your part 1 solution, but the real input has no such lines.

The trick to fixing this with regex was to switch from "\d|one|two|..." to "(?=(\d|one|two|...))". This is a regex lookahead and allows us to match each match without "consuming" the digits to the right, leaving them available to be rematched.