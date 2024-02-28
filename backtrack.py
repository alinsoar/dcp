
def backtrack(s, n, m):

    def reject(s):
        a = [0] * m
        for i in s: a[i] += 1
        return any([x > 1 for x in a])

    def accept(s):
        if len (s) == n:
            a=s[:]
            res.append(a)

    def first(s):
        n = s+[0]
        if (len (n) > n):
            return None
        else:
            return n

    def next (s):
        s[-1] += 1
        if s[-1] < m: return s
        else: return None


    if (reject (s)): return
    if (accept (s)): output (s)
    w = first (s)
    while w:
        backtrack(w, n, m)
        w = next (w)

res = []
backtrack([],2,4)
for i in res: print i


