The hardest day by far and the first I had to abandon.

This is basically picross.

For part 1, we have q question marks and we can figure out how many we need to fill in by taking the sum of the numbers on the side and subtracting the number of #s we already have. Then I just brute forced the `(possible indices) choose q` possibilities.

This is way too slow for part 2. Like way too slow.

So I rewrote it painfully to use a new data structure: I keep the "paths" (which are just a sorted sequence of question-mark indices to turn into #s) in a sorted nested spot in the structure, so if we were considering [0,1,4] and [0,1,5], it would look like {0: {1: {4: None, 5: None}}}. Then when we're evaluating a path, we evaluate it incrementally. If I find that [1,2] doesn't work, I can delete tree[1][2] from my data structure and it will delete all paths that start with that prefix.

The problem is that i need to populate the tree ahead of time with all (possible indices) choose (num question marks) paths. Python's combinations function does the work of generating them but for something like 40 choose 20, this is just wayyyyyy too big. What we really need is a method to not even *generate* paths with deadend prefixes. I couldn't figure it out.