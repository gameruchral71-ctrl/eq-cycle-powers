"""Fractional equivalence covering number of C_n^k via the rotation-invariant dual:
max n*sum_d y_d  s.t. every partition into cliques has sum of y_{dist} over covered pairs <= 1."""
import sys, itertools, numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from eqsat import edges
def dist(n,a,b): d=abs(a-b); return min(d,n-d)
def pricing(n,k,y):
    E=edges(n,k); idx={e:i for i,e in enumerate(E)}; m=len(E)
    adj={v:set() for v in range(n)}
    for u,v in E: adj[u].add(v); adj[v].add(u)
    rows=[];ub=[]
    for v in range(n):
        for a,b in itertools.combinations(sorted(adj[v]),2):
            ea=idx[tuple(sorted((v,a)))]; eb=idx[tuple(sorted((v,b)))]; ab=tuple(sorted((a,b)))
            r=np.zeros(m); r[ea]=1; r[eb]=1
            if ab in idx: r[idx[ab]]=-1
            rows.append(r); ub.append(1)
    c=-np.array([y[dist(n,*e)-1] for e in E])
    res=milp(c,constraints=LinearConstraint(np.array(rows),-np.inf,np.array(ub)),integrality=np.ones(m),bounds=Bounds(0,1))
    z=np.round(res.x).astype(int)
    cnt=[0]*k
    for e,zi in zip(E,z):
        if zi: cnt[dist(n,*e)-1]+=1
    return -res.fun, cnt
def frac(n,k):
    cols=[]   # each column: counts of covered pairs per distance
    # start: the "all windows" style bound: y_d <= something; seed with single-distance partitions
    y=np.ones(k)/n
    for it in range(200):
        val,cnt=pricing(n,k,y)
        if val<=1+1e-9 and it>0: break
        cols.append(cnt)
        A=np.array(cols,dtype=float)
        res=linprog(-n*np.ones(k),A_ub=A,b_ub=np.ones(len(cols)),bounds=[(0,None)]*k,method='highs')
        y=res.x
    return n*y.sum(), y
if __name__=='__main__':
    k=int(sys.argv[1])
    for n in map(int,sys.argv[2:]):
        f,y=frac(n,k); print('k=%d n=%d frac=%.4f'%(k,n,f), np.round(y*n,3), flush=True)
