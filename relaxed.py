"""Relaxed system H(m) for the every-k induction.
On Z_n: one tight set S_v (level m) with left end v for every v; each class gets a colour from C
(|C| = m+1+extra); classes of one colour are disjoint; every vertex lies in exactly m+1 classes;
all pairs at distance <= k covered; the set M(v) of colours missing at v satisfies M(v) = M(v+N).
extra = 0 is exactly an (m+1)-layer cover. Question: does H(m) force N | n?
Usage: python3 relaxed.py m extra n1 n2 ..."""
import sys, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from tight import tight_sets
m=int(sys.argv[1]); extra=int(sys.argv[2]); N=2**m; k=N-1
TS=[frozenset(S) for S in tight_sets(m)]; C=m+1+extra
def solve(n):
    pool=IDPool(); cl=[]
    y=lambda v,s: pool.id(('y',v%n,s)); z=lambda v,c: pool.id(('z',v%n,c))
    # u[x,c]: colour c present at vertex x
    u=lambda x,c: pool.id(('u',x%n,c))
    def exactly(lits,b):
        cl.extend(CardEnc.equals(lits,bound=b,vpool=pool,encoding=EncType.seqcounter).clauses)
    for v in range(n):
        exactly([y(v,s) for s in range(len(TS))],1); exactly([z(v,c) for c in range(C)],1)
    # inc[v,x]: class v contains x (x-v = d in 0..k)
    inc=lambda v,d: pool.id(('inc',v%n,d))
    for v in range(n):
        for d in range(k+1):
            ss=[s for s in range(len(TS)) if d in TS[s]]
            cl.append([-inc(v,d)]+[y(v,s) for s in ss])
            for s in ss: cl.append([inc(v,d),-y(v,s)])
    for x in range(n):
        exactly([inc(x-d,d) for d in range(k+1)],m+1)
        for c in range(C):
            # u(x,c) <-> OR_d (inc(x-d,d) & z(x-d,c)); at most one such (disjointness)
            terms=[]
            for d in range(k+1):
                t=pool.id(('t',x,d,c)); terms.append(t)
                cl += [[-t,inc(x-d,d)],[-t,z(x-d,c)],[t,-inc(x-d,d),-z(x-d,c)]]
            cl.extend(CardEnc.atmost(terms,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
            cl.append([-u(x,c)]+terms)
            for t in terms: cl.append([u(x,c),-t])
            cl += [[-u(x,c),u(x+N,c)],[u(x,c),-u(x+N,c)]]
        # pairs (x, x+d) covered
        for d in range(1,k+1):
            lits=[]
            for e in range(0,k-d+1):   # class with left end x-e contains x and x+d
                v=x-e
                ss=[s for s in range(len(TS)) if e in TS[s] and e+d in TS[s]]
                lits += [y(v,s) for s in ss]
            cl.append(lits)
    s=Cadical153(bootstrap_with=cl); r=s.solve(); s.delete(); return r
for n in map(int,sys.argv[3:]):
    print('m=%d extra=%d n=%d %s'%(m,extra,n,'SAT' if solve(n) else 'UNSAT'),flush=True)
