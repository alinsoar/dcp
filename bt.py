
def bt(c, n, m):

    def reject(c):
        if len(c) > n: return False
        a = [0]*m
        for i in c: a[i]+=1
        return any ([x > 1 for x in a]) or (sorted(c) != c)


    def accept(c):
        return len(c) == n


    def output(c):
        for i in c: print i,
        print


    def first(p,c):
        if len(c)<n: return c[:]+[0]
        else: return None


    def next(p,s):
        s[-1] += 1
        if (s[-1] < m): return s
        else: return None


    if reject(c): return
    if accept(c): output(c)
    s = first(0,c)
    while s != None:
        bt(s, n, m)
        s = next(0,s)

bt([], 3, 10)



