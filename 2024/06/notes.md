for part 1, we're navigating a grid and turning when we hit obstacles. it's straight forward to navigate and count how many squares we hit before we leave the board.

for part 2, we need to determine which locations we could put obstacles in to create infinite loops.
- naive: try everywhere except starting position (29s)
- smarter: try only places visited, except starting position (5s)
- smartest: try only places visited, except starting position, AND when checking for loops start the guard only at the location right before the obstacle. i couldn't get this working for a long time because I wasn't considering the possibility that I might be checking the scenario "obstacle at ox, oy, guard at x, y (right before obstacle)" in situations where the guard could have only ever gotten to x, y if the obstacle had not been at (ox, oy). This was fixed by simply making sure to never double-check an obstacle position.