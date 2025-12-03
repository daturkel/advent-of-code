The solution from part 1 teaches you the general idea you need: get the maximum of the list of digits but leave room off the right side because we can't use the right-most digit as our *first* digit (since there will be nothing left as the second digit). Generalizing that, we leave off a shrinking number of digits on the right end as we progressively get the highest digit.

4ms