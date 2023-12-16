today is bullshit because the answer is easy if you make certain assumptions that you have no good reason to make. i discovered/validated these in a separate python notebook:
a) paths from all XXA nodes create cycles
b) paths from all XXA nodes create cycles which visit an XXZ node infinitely many times
c) paths from XXA nodes only visit a single unique XXZ node
c) paths from XXA nodes visit XXZ nodes in the same number of steps each time (i.e. if first time til XXZ takes n steps, second time takes 2n steps)
Once you know this, you can just calculate cycle lengths for each starting node, and then the solution is lcm(cycle lengths).
Any python has math.lcm built in which is nice