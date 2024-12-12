This is an area bounding problem. I was very preoccupied assuming I would have to dedupe edges, but this wasn't required.

For part 1, we flood fill to get the area and edges simultaneously. Edges are represented as a point and a direction (x,y,"N"). 

For part 2, we consider all the edges we selected. For a given edge, we check to see if we have the edges next to it, removing them from the edge list if we do. Once we're out of neighboring edges, that's the end of that side, and we start with a new edge and thus a new side.

Originally I had canonicalized edge representations so that there was never two ways of representing the same edge (i.e. 0,0,"E" and 1,0,"W"). This turned out to be a bad idea, because it means you can't distinguish that a side south of Y actually does not count as the same side north of Y+1. Removing the canonicalization code fixed this.

AAAAAA
AAABBA
AAABBA < see the problem here?
ABBAAA
ABBAAA
AAAAAA