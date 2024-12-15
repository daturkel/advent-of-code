this was a tricky day. we have to move around a maze pushing blocks.

in part 1, the blocks are 1x1, so moving them is straight forward. I used a recursive method which checks to see if a rock can be moved (including possibly pushing the next rock in front of it).

in part 2, the blocks are 2x1, which means now each rock could potentially move 2 rocks (if moving vertically). I thought at first that I could no longer do a recursive method because I kept getting recursion limits, but it turns out that that's just because I had infinite loops because I was hitting a \[, checking the \] to the right, then the \[ to the left, forever. Adding a check to make sure we don't move backwards allows the recursive method to work just fine.