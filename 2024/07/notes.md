we have a value and a list of numbers and we don't know how to combine those numbers with + and * to get the value.

I iterate through all ordered combinations of the operators and stop if I reach one that solves it.

In part two, we add a concatenation operator.

A smarter way to do this would be to do DFS to build up the list of operators where we prefer times and plus over cat, since using product to generate the list of operations comes up with a less than ideal ordering.