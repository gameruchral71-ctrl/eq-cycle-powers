"""Is eq(C_n^k) <= t ?  SAT encoding: each edge gets >=1 of t layers; each layer is a disjoint union of cliques."""
import sys, itertools, time
from pysat.solvers import Cadical153
def edges(n,k):
    E=set()
    for v in range(n):
        for d in range(1,k+1): E.add(tuple(sorted((v,(v+d)%n))))
    return sorted(E)
def solve(n,k,t,symm=True):
    E=edges(n,k); idx={e:i for i,e in enumerate(E)}
    var=lambda e,l: 1+idx[e]*t+l
    adj={v:set() for v in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    s=Cadical153()
    for e in E: s.add_clause([var(e,l) for l in range(t)])
    for l in range(t):
        for v in range(n):
            for a,b in itertools.combinations(sorted(adj[v]),2):
                ea=tuple(sorted((v,a))); eb=tuple(sorted((v,b)))
                ab=tuple(sorted((a,b)))
                if ab in idx: s.add_clause([-var(ea,l),-var(eb,l),var(ab,l)])
                else: s.add_clause([-var(ea,l),-var(eb,l)])
    if symm: s.add_clause([var(E[0],0)])  # layers are interchangeable
    r=s.solve()
    model=s.get_model() if r else None
    layers=None
    if r:
        ms=set(x for x in model if x>0)
        layers=[[e for e in E if var(e,l) in ms] for l in range(t)]
    s.delete()
    return r, layers
if __name__=='__main__':
    k=int(sys.argv[1])
    for n in range(2*k+2, int(sys.argv[2])+1):
        lo=None
        for t in range(1,12):
            t0=time.time(); r,_=solve(n,k,t)
            if r: print('k=%d n=%d eq=%d (%.1fs)'%(k,n,t,time.time()-t0),flush=True); break
