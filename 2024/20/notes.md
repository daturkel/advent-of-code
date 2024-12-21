Part 1 is easy enough: for each path in a maze, we check its two-hop neighbors and see how much time we would save by skipping to there.

For part 2, I just check the distance between step i and step j where j > i (thus quadratic complexity). We check to see how much was saved and whether or not we can skip from one to the other in less than or equal to 20 steps.