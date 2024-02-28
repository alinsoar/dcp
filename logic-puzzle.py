"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."

    import itertools as it

    def gen(N):
        comb = it.permutations (D.values(), N)
        for x in comb: yield x

    names = ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI']

    D = dict([[y,x] for x,y in enumerate(days,1)])

    R = [ [Hamming, Knuth, Minsky, Simon, Wilkes]
        for (Hamming, Knuth, Minsky, Simon, Wilkes) in gen (5)  # 
        if Knuth == Simon + 1                                   # F6
        for (programmer, writer, designer, manager)  in gen (4) # 
        if Knuth == manager + 1                                 # F10
        if designer != D['THU']                                 # F7
        if Knuth != manager                                     # F5
        if writer != Minsky                                     # f4
        if Wilkes != programmer                                 # F2
        for (laptop, droid, tablet, iphone) in gen (4)          # 
        if iphone == D['TUE'] or tablet == D['TUE']             # F12
        if {laptop, Wilkes} == {D['MON'], writer}               # F11
        if designer != droid                                    # F9
        if tablet != D['FRI']                                   # F8
        if tablet != manager                                    # F5
        if {droid, programmer} == {Hamming, Wilkes}             # F3
        if laptop == D['WED']                                   # F1
    ]

    print R

    res = [None]*len(D)
    for x in range (len(D)):
        print x, names[x], R[0], res
        res[R[0][x]-1] = names[x]

    print res

logic_puzzle()
