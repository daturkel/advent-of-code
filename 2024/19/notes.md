This is some leetcode stuff. For part 1, we look at every prefix of the current string. If it's in the allowable tokens, we pop it off the string and recurse on the remaining bit of the string until the string is empty. That means that string can be built out of the tokens.

For part 2, we do the same but we don't short-circuit: just count how many ways we can do it.

For both parts, a cache is essential in keeping the solution extremely fast.