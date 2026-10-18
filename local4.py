import itertools
T=['A1','B2','W1','W2']
def ok(seq):
    n=len(seq); I=lambda v: seq[v%n]
    for v in range(n):
        if I(v)=='W1' and I(v+1)!='W2': return False
        if I(v)=='W2' and I(v-1)!='W1': return False
        c=(I(v)=='A1')+(I(v+2)=='B2')+(I(v+1)=='W1')+(I(v)=='W1')
        if c!=1: return False
        if not (I(v) in ('B2','W1','W2') or I(v+1) in ('A1','W1')): return False
    return True
for n in range(4,17):
    sols=[s for s in itertools.product(T,repeat=n) if ok(s)] if n<=12 else None
    if sols is not None: print(n,len(sols), sols[:3])
