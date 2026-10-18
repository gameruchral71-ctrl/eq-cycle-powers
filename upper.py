"""Upper-bound witnesses: for each n, find a cover of C_n^k by t equivalence layers
(t=m+1 if (k+1)|n else m+2), check it independently, and save it."""
import sys, json, os, time, itertools
from eqsat import solve, edges
def check(n,k,layers):
    E=set(edges(n,k)); cov=set()
    for L in layers:
        adj={}
        for u,v in L: adj.setdefault(u,set()).add(v); adj.setdefault(v,set()).add(u)
        for v in adj:   # neighbourhood of v plus v is a clique => layer is a disjoint union of cliques
            for a,b in itertools.combinations(adj[v],2):
                if tuple(sorted((a,b))) not in set(map(tuple,L)): return False
        cov|=set(map(tuple,L))
    return cov>=E
k=int(sys.argv[1]); lo,hi=int(sys.argv[2]),int(sys.argv[3]); N=k+1; m=N.bit_length()-1
os.makedirs('witness',exist_ok=True)
for n in range(lo,hi+1):
    t=m+1 if n%N==0 else m+2
    t0=time.time(); r,layers=solve(n,k,t)
    ok=r and check(n,k,layers)
    if ok: json.dump(layers,open('witness/k%d_n%d.json'%(k,n),'w'))
    print('k=%d n=%d t=%d %s %.1fs'%(k,n,t,'VERIFIED' if ok else 'FAIL',time.time()-t0),flush=True)
