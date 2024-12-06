for part 1, we're navigating a grid and turning when we hit obstacles. it's straight forward to navigate and count how many squares we hit before we leave the board.

for part 2, we need to determine which locations we could put obstacles in to create infinite loops.
- naive: try everywhere except starting position (29s)
- smarter: try only places visited, except starting position (5s)
- smartest: try only places visited, except starting position, AND when checking for loops start the guard only at the location right before the obstacle. for some reason I couldn't get this working but it should've brought me down to 1-2s.