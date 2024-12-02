A tricky day: determine if a list of numbers follows some rules: every list must be ascending or descending, with all differences between 1 and 3.

In part 2, we're allowed to remove one index to make it work.

I tried to be clever, only removing the indices necessary for each rule violation. Turns out brute forcing wouldn't have taken very long at all.

Had to use make sure my code passes [this reddit post of edge cases](https://www.reddit.com/r/adventofcode/comments/1h4shdu/2024_day_2_part2_edge_case_finder/) to fix my cleverness. In rust solution, I just brute forced.