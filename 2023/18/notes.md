For today, I copied my logic from day 10 for detecting inner and outer pieces, though instead of starting at a point and heading outward, I just scan left to right on each row. This works, but it's way too slow for part 2.

---

Second attempt, I found a reddit comment mentioning using the shoelace formula and pick's theorem. I had never heard of either of them but they make the problem trivial.

One weird thing is that I encountered this issue for the first time while annotating `get_border`: https://stackoverflow.com/a/76765708 (though this doesn't remain in the final solution)

I reduced time from 52 seconds to 23 seconds by calculating the length of the border and calculating the area simultaneously, rather than building up a list of border pieces and calculating area after. This way we avoid expensive calls to list.append.