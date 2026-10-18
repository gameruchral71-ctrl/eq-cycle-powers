import itertools, sys
from pysat.solvers import Cadical153
from eqsat import edges
def all_solutions(n,k,t,limit=2000):
    E=edges(n,k); idx={e:i for i,e in enumerate(E)}
    var=lambda e,l: 1+idx[e]*t+l
    adj={v:set() for v in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    s=Cadical153()
    for e in E: s.add_clause([var(e,l) for l in range(t)])
    for l in range(t):
        for v in range(n):
            for a,b in itertools.combinations(sorted(adj[v]),2):
                ea=tuple(sorted((v,a))); eb=tuple(sorted((v,b))); ab=tuple(sorted((a,b)))
                s.add_clause([-var(ea,l),-var(eb,l)] + ([var(ab,l)] if ab in idx else []))
    sols=[]
    while len(sols)<limit and s.solve():
        m=set(x for x in s.get_model() if x>0)
        layers=[frozenset(e for e in E if var(e,l) in m) for l in range(t)]
        sols.append(layers)
        s.add_clause([-x for x in m if x<=len(E)*t])  # block exact assignment
    return sols
def classes(n,layer):
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for u,v in layer: par[f(u)]=f(v)
    cl={}
    for v in range(n): cl.setdefault(f(v),[]).append(v)
    return list(cl.values())
def is_tiling(n,k,layer):
    cs=classes(n,layer)
    return all(len(c)==k+1 for c in cs)
if __name__=="__main__":
  n,k,t=map(int,sys.argv[1:4])
  sols=all_solutions(n,k,t)
  cnt=sum(any(is_tiling(n,k,L) for L in sol) for sol in sols)
  print(n,k,t,'solutions examined',len(sols),'with a full-window tiling layer',cnt)
