"""Local analysis: sequence L(v) of tight types (class with left end v), constraints:
 each vertex in exactly m+1 classes; weighted pairs exactly once; all pairs at distance<=k at least once.
Build the de Bruijn-style graph of valid k-windows and report its strongly connected structure."""
import sys, itertools
from tight import tight_sets, weights
sys.setrecursionlimit(1000000)
m=int(sys.argv[1]); N=2**m; k=N-1; w=weights(m)
T=tight_sets(m); TS=[frozenset(S) for S in T]
# constraint at vertex v involves types at v-k..v (classes containing v or pairs starting at v-?).
# We check, for the window types t[0..k] = L(v-k..v), the constraints "centred" at vertex v (=index k):
#  - count of classes containing v: sum over i: (k - i) in TS[t[i]]  ... class L(v-k+i) contains v iff (k-i) in S
#  - pairs (v-d, v)?? use pairs ending at v: pair (v-d, v) is in class L(u) iff u<=v-d and (v-d-u),(v-u) in S
def ok(win):
    # win: tuple of k+1 type indices for L(v-k),...,L(v)
    cnt=sum(1 for i in range(k+1) if (k-i) in TS[win[i]])
    if cnt!=m+1: return False
    for d in range(1,k+1):
        c=0
        for i in range(k+1-d):   # u = v-k+i, need u<=v-d
            S=TS[win[i]]
            if (k-i) in S and (k-i-d) in S: c+=1
        if w[d]>0 and c!=1: return False
        if c<1: return False
    return True
# DFS over windows: state = last k types; extend by next type, check ok(state+next)
from collections import defaultdict
idx=range(len(T))
# prefix pruning: partial checks are hard; brute force for m=2, smarter for m=3
states=set(); edges=defaultdict(set)
if m==2:
    for win in itertools.product(idx,repeat=k+1):
        if ok(win): edges[win[:-1]].add(win[1:])
else:
    # incremental: necessary condition on partial windows: count of classes containing v so far <= m+1, pair counts for weighted <=1
    def partial_ok(pre):
        j=len(pre)-1  # pre = L(v-k..v-k+j); check vertex x=v-k+j's constraints that only involve u<=x: none complete.
        return True
    # we instead build windows by DFS over positions and test full window
    cnt=0
    def rec(pre):
        global cnt
        if len(pre)==k+1:
            if ok(tuple(pre)): edges[tuple(pre[:-1])].add(tuple(pre[1:]))
            return
        # pruning: vertex v-k+len(pre)-1 ... skip
        for t in idx:
            pre.append(t); rec(pre); pre.pop()
    print('too big without pruning'); sys.exit()
nodes=set(edges)|{x for s in edges.values() for x in s}
print('m',m,'valid windows',sum(len(s) for s in edges.values()),'states',len(nodes))
# strongly connected components via iterative Tarjan
import itertools as it
index={};low={};onst=set();st=[];comps=[];c=[0]
def strong(v):
    stack=[(v,iter(edges.get(v,())))]; index[v]=low[v]=c[0]; c[0]+=1; st.append(v); onst.add(v)
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
for v in nodes:
    if v not in index: strong(v)
for comp in comps:
    cs=set(comp)
    if len(comp)==1 and comp[0] not in edges.get(comp[0],()): continue
    ne=sum(1 for u in comp for x in edges.get(u,()) if x in cs)
    print('SCC size',len(comp),'internal edges',ne, [tuple(T[i] for i in s) for s in comp][:4])
