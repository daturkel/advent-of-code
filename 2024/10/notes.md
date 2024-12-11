First we need to see how many 9s we can reach from each 0, and then we need to see how many unique ways we can reach any 9 from each 0.

I used recursive DFS for both parts. We find all unique paths from each 0 to any 9 and keep track of both the number of unique paths as well as the unique end points. We use a cache in the recursive function to speed up the search from ~8ms to ~4ms.