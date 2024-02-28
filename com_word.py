# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)' 
# Non-uppercase words should remain unchaged.

import string

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    # Your code here.
    def split(w, L):
        if w == "":
            return L
        elif w[0] in string.ascii_uppercase:
            i = 0
            while(i < len(w) and w[i] in string.ascii_uppercase):
                i += 1
            n = L + [w[:i]]
            return split(w[i:], n)
        else:
            return split(w[1:], L+[w[0]])

    def compile(w):
        r= ["*".join([str(x),str(y)]) for x,y in zip(w[::-1], [10**i for i in range(len(w))])]
        return "+".join(r)

    r = []
    for x in split(word, []):
        if (x[0] in string.ascii_uppercase):
            r.append(compile(x))
        else:
            r.append(x)
    return "".join(r)



