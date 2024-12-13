This problem is about finding the right number of button presses to get a crane over a prize. Button A moves you ax,ay and button B moves you bx,by—however, button A costs 3 to press while button B costs only 1. What's the cheapest way to get to px py?

It's a huge misdirect to suggest that the solver needs to find the cheapest way: this is a system of 2 equations with two unknowns, so there's 0, 1, or infinite solutions. In these systems, there's always 1 solution. Use your preferred method of solving a system and then just return 3*a + b. (If the solution is not integral, toss it out since there's no fractional button presses.)

For part two, we make the px and py coordinates much bigger, but this doesn't matter because our solution is constant time.