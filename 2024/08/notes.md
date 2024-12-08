We need to find points with the same letter, calculate the vector between them, and then extend that line in both directions within the bounds of the map. For part 1, we only need to go one in each direction. For part 2, we go as far as we can.

We use combinations to find the unique pairs of nodes to extend. Then we just add and subtract the delta between them while doing bounds checking.