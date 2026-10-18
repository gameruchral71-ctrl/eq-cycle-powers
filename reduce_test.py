"""Test the decimation step of the proposed induction H(m) -> H(m-1).
Enumerate H(m) systems with relaxed.py's encoding, then try: keep the vertices of one parity
(optionally after reflecting x -> -x), restrict every class to them, drop singletons, halve.
Check the result is an H(m-1) system on n/2 vertices.  Usage: python3 reduce_test.py m extra n limit"""
import sys, itertools
from pysat.solvers import Cadical153
from tight import tight_sets, weights
import relaxed_lib as R
m,extra,n,limit=map(int,sys.argv[1:5])
TS1=set(frozenset(S) for S in tight_sets(m-1)) if m>=2 else None
def check_H(n,m,classes,C):
    """classes: list of (set of vertices, colour). H(m) check without the one-per-left-end bookkeeping."""
    N=2**m; k=N-1; tight=set(frozenset(S) for S in tight_sets(m)) if m>=2 else {frozenset({0,1})}
    left={}
    for V,c in classes:
        # find left end a with V-a within [0,k] containing 0 and k
        ok=False
        for a in V:
            rel=frozenset((x-a)%n for x in V)
            if max(rel)<=k and frozenset(rel) in tight: ok=True; break
        if not ok or a in left: return 'bad class/left end'
        left[a]=(V,c)
    if len(left)!=n: return 'not one per left end'
    cnt=[0]*n; cols=[set() for _ in range(n)]
    for V,c in classes:
        for x in V:
            cnt[x]+=1
            if c in cols[x]: return 'colour clash'
            cols[x].add(c)
    if any(t!=m+1 for t in cnt): return 'count'
    M=[frozenset(range(C))-cols[x] for x in range(n)]
    if any(M[x]!=M[(x+N)%n] for x in range(n)): return 'M not periodic'
    for x in range(n):
        for d in range(1,k+1):
            if not any(x in V and (x+d)%n in V for V,_ in classes): return 'uncovered'
    return 'ok'
def reduce(n,classes,par,refl):
    out=[]
    for V,c in classes:
        W=[((-x)%n if refl else x) for x in V]
        E=[x for x in W if x%2==par]
        if len(E)>=2: out.append((frozenset(((x-par)//2)%(n//2) for x in E),c))
    return out
cnt=0; res={}
for n_,classes,C in R.enumerate_systems(m,extra,n,limit):
    assert check_H(n,m,classes,C)=='ok'
    outcomes=tuple(check_H(n//2,m-1,reduce(n,classes,p,r),C) for p in (0,1) for r in (0,1))
    good=any(o=='ok' for o in outcomes)
    res[good]=res.get(good,0)+1
    if not good and res[good]<=3: print('FAIL', outcomes, sorted((tuple(sorted(V)),c) for V,c in classes)[:8])
    cnt+=1
print('m=%d extra=%d n=%d systems %d reducible: %s'%(m,extra,n,cnt,res))
