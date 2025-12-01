Part one is trivially easy to keep track of current position and check if it's 0.

Part two is surprisingly annoying. In the end, I got it working by looking at the magnitude of each turn. |turn| // 100 is the number of "guaranteed" zero-passes in that turn, but we also have to consider any extra zero passes that occur as a side-effect of our starting position. |turn| % 100 gives us the remaining amount of turn after considering the "guaranteed" passes. If we're going left and this amount is more than our current position, then that's one extra turn. If we're going right and this amout is more than our current position (and our current position is not 0), then that's one extra turn.

Total time is just a little over 1ms.
