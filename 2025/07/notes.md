A tricky day! Part 1 is easy enough on its own: keep track of every time you split, without duplicates.

Part 2 requires you to rethink. I did a DFS but it was too slow for part 2. Instead, I went with a bookkeeping solution that tracks how many paths you can take to each point in the 2d grid. Then we add up all the paths for each point in the bottom row.