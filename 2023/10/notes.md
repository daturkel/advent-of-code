This one is hard!
Part 1 is straightforward enough: locate the starting point, determine which directions it can go, then travel the loop. The furthest distance is the point about halfway through the loop.

For part 2, we use the border we built up in part 1. For every element on the grid that's not on the border, we travel straight until we hit the edge. If we cross the border an even number of times then we're outside and if we cross an odd number then we're inside.

The tricky part is what happens if you travel *along* a border? It turns out there are two cases:
- you can travel along a border and not cross it, like `F----7` travling east or west
- or you can travel a long a border and actually cross it, like `F----L` traveling east or west

I made a note of when we "entered" and "exited" the border. If the entrance and exit were {|}, {-}, {F,J}, or {L,7} then we crossed the border. Using this logic we count crossings as usual and check how many crossings we did at the end.

As a small optimization, we can avoid going all the way to the edge if we hit a known inside or outside piece. If we hit an inside in an even number of crossings, we're in, and if it's odd we're out. If we hit an outside in an even number of crossings, we'rre out, and if it's odd we're in.