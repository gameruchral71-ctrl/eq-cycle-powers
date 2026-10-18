"""Layered local scan. In an (m+1)-layer cover of C_n^k (k=2^m-1) every class is tight and
exactly one class has left end v, for each v. Type of v = (tight set S, layer). Constraints:
each vertex lies in exactly one class of each layer; each pair at distance d<=k is covered,
exactly once if d has positive weight. Build the de Bruijn graph of valid (k+1)-windows and
report, per strongly connected component, the gcd of its cycle lengths."""
import sys, math
from collections import defaultdict
from tight import tight_sets, weights
sys.setrecursionlimit(100000)
m=int(sys.argv[1]); N=2**m; k=N-1; w=weights(m); L=m+1
T=[(S,l) for S in tight_sets(m) for l in range(L)]
W=2*k+1
edges=defaultdict(set); nwin=0
cov=[[0]*W for _ in range(L)]          # cov[layer][pos]
pc=defaultdict(int)                     # (pos_a,pos_b) -> cover count, weighted pairs only
win=[]
def add(t,j,sign):
    S,l=T[t]
    for s in S: cov[l][j+s]+=sign
    for a in S:
        for b in S:
            if a<b and w[b-a]>0: pc[(j+a,j+b)]+=sign
def okadd(t,j):
    S,l=T[t]
    for s in S:
        if cov[l][j+s]: return False
    for a in S:
        for b in S:
            if a<b and w[b-a]>0 and pc[(j+a,j+b)]: return False
    return True
def final():
    v=k
    for l in range(L):
        if cov[l][v]!=1: return False
    for d in range(1,k+1):
        if not any(v-d-j in T[win[j]][0] and v-j in T[win[j]][0] for j in range(v-d+1)): return False
    return True
def rec(j):
    global nwin
    if j==k+1:
        if final(): edges[tuple(win[:-1])].add(tuple(win[1:])); nwin+=1
        return
    for t in range(len(T)):
        # symmetry: first window position uses layer 0 only up to relabelling? no: keep all labels
        if okadd(t,j):
            add(t,j,1); win.append(t)
            # vertex j-? : vertex at pos j is complete only if j==k; prune: vertex j must be coverable later - skip
            rec(j+1)
            win.pop(); add(t,j,-1)
rec(0)
print('m',m,'types',len(T),'valid windows',nwin,flush=True)
# trim to nodes on bi-infinite paths
nodes=set(edges)|{x for s in edges.values() for x in s}
changed=True
while changed:
    changed=False
    indeg=defaultdict(int)
    for u in list(edges):
        edges[u]={x for x in edges[u] if x in nodes}
        if not edges[u]: del edges[u]
    for u in edges:
        for x in edges[u]: indeg[x]+=1
    keep={u for u in nodes if u in edges and indeg[u]>0}
    if keep!=nodes: nodes=keep; changed=True
print('nodes after trim',len(nodes),flush=True)
# SCCs (iterative Tarjan) and period of each
index={};low={};onst=set();st=[];comps=[];c=[0]
for v0 in nodes:
    if v0 in index: continue
    stack=[(v0,iter(edges.get(v0,())))]; index[v0]=low[v0]=c[0]; c[0]+=1; st.append(v0); onst.add(v0)
    while stack:
        u,itr=stack[-1]
        for x in itr:
            if x not in index:
                index[x]=low[x]=c[0]; c[0]+=1; st.append(x); onst.add(x); stack.append((x,iter(edges.get(x,())))); break
            elif x in onst: low[u]=min(low[u],index[x])
        else:
            stack.pop()
            if stack: low[stack[-1][0]]=min(low[stack[-1][0]],low[u])
            if low[u]==index[u]:
                comp=[]
                while True:
                    x=st.pop(); onst.discard(x); comp.append(x)
                    if x==u: break
                comps.append(comp)
for comp in comps:
    cs=set(comp)
    if len(comp)==1 and comp[0] not in edges.get(comp[0],()): continue
    lev={comp[0]:0}; q=[comp[0]]; g=0
    for u in q:
        for x in edges.get(u,()):
            if x not in cs: continue
            if x not in lev: lev[x]=lev[u]+1; q.append(x)
            else: g=math.gcd(g,lev[u]+1-lev[x])
    ex=comp[0]
    print('SCC size',len(comp),'period',g,'example',[ (T[t][0],T[t][1]) for t in ex])
