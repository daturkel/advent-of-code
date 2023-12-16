Part 1 is trivial.

For part 2, the trivial solution also works, but it takes 6 seconds. They probably should've made the inputs so big that the trivial solution isn't feasible at all, but oh well.

I wasn't happy with 6 seconds though, so I sought a better solution.

We want to know how many integral solutions there are to the inequality
(time - charge) * speed ≥ record

Since speed is charge, then this is just:
(time - charge) * charge - record ≥ 0
-charge^2 + time*charge - record ≥ 0

Since the "a" of our quadratic inequality is negative, then we care about the values of charge *between* the two roots. (If a was positive, we would want values below the lower root and above the higher root, of which there would be an infinite number.) So all we have to do is solve the quadratic equation -charge^2 + time*charge - record = 0 (solving for charge). Then we round up the lower root and round down the higher root, since we only care about integral solutions, and the number of solutions to the inequality is upper_rounded_root - lower_rounded_root + 1.

After figuring that out, I went back and changed my part 1 solution to use the same thing, though it makes basically no difference since the numbers for part 1 are so small.