use djikstra's for part 1. it was only finding one path for a long time because i was tracking distances as distant to a point, rather than distance to a point *from a direction*. once i added the direction to my distance dictionary, i had all paths to the end.

from there, i could just trace all paths backwards and accumulate the number of unique points