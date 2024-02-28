#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools


def floor_puzzle():
    floors = range(1,6)

    def c(f):
        for x in f:
            print ':',x
            yield x

    def top(floor):
        return floor == floors[-1]

    def bottom(floor):
        return floor == floors[0]

    def highter(f1, f2):
        return (f1 > f2)

    def adjacent(f1, f2):
        return abs(f2-f1) == 1

    def diff(a,b,c,d,e):
        s = set([a,b,c,d,e])
        return len(s) == 5

    # Your code here
    res = [(Hopper, Kay, Liskov, Perlis, Ritchie)] = [
        (Hopper, Kay, Liskov, Perlis, Ritchie)
        for Hopper in floors
        # Hopper does not live on the top floor.
        if not top(Hopper)
        for Kay in floors
        # Kay does not live on the bottom floor.
        if not bottom(Kay)
        for Liskov in floors
        # Liskov does not live on either the top or the bottom floor.
        if not top(Liskov) and not bottom(Liskov)
        if not adjacent(Liskov, Kay)
        for Perlis in floors
        # Perlis lives on a higher floor than does Kay.
        if highter(Perlis, Kay)
        for Ritchie in floors
        # Ritchie does not live on a floor adjacent to Liskov's.
        if not adjacent(Ritchie, Liskov)
        # Liskov does not live on a floor adjacent to Kay's.
        if diff(Hopper, Kay, Liskov, Perlis, Ritchie)]
    for x in res: print x
    return [Hopper, Kay, Liskov, Perlis, Ritchie]

floor_puzzle()
