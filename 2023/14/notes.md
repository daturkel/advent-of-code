For part 1, I considered how my design might need to change depending on what part 2 looked like. I decided to implement the ability to shift in *any* direction, which paid off for part two as it became simple to implement the spin cycle.

However running one billion spin cycles turned out to be too slow. It was going to take 53 days to finish.

I printed each iteration's graph and watched each spin cycle until I found that they end up in a loop pretty quickly. All that was left was to figure out where the loop starts and how long it is, keeping track of the grid at every time step so far. Then with a little fancy indexing to figure out which possible grid we'd be at at t=1b, we're done.

The reason mine is slowish (2-3 seconds) is because my shifting code is slow—i move each stone one unit at a time. I could move it as many units as it needed to move at a time by using a sparse data structure instead of checking each position to see if I can move there, but I'm not really worried about the optimization.