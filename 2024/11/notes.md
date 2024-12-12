We need to track a system of cellular automata after 25 and after 75 steps. After 25 is reasonable to do manually applying the rules (my original solution for part 1), but 75 grows way too big.

To make this tractable for part 2, I replaced a for loop with a recursive function with a cache. This takes advantage of the fact that many numbers occur many times.

My cache is keyed on (number, units of time remaining), so it only has cache hits for duplicate numbers in the same iteration. Another way to do this would be to track the result for each starting number after N units of time have *passed*. This way, if you encounter 0 in the first time step, you'd get cache entries for (0, 75), (0, 74), (0, 73...) that you could use at every future time stamp whenever you encounter a 0. However, with part two working in ~65ms, this optimization was not needed (and it would've led to a massive cache anyway).