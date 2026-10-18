"""Transfer graph via SAT. A k-tuple of types lying on a cycle of the transfer graph G_m sits in the
middle of arbitrarily long valid paths. We enumerate (with blocking clauses) every k-tuple that occurs
at positions [c, c+k) of some valid path of P types (local conditions imposed at every vertex v with
k <= v < P). Restricted to these tuples, G_m keeps all of its cyclic strongly connected components;
we then compute their periods.  Usage: python3 satscan.py m P c"""
import sys, math, time, pickle
from collections import defaultdict
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from tight import tight_sets, weights
m=int(sys.argv[1]); P=int(sys.argv[2]); c=int(sys.argv[3])
N=2**m; k=N-1; w=weights(m); L=m+1
T=[(frozenset(S),l) for S in tight_sets(m) for l in range(L)]
pool=IDPool(); x=lambda v,t: pool.id(('x',v,t))
cl=[]
def card(lits,lo,hi):
    if hi is not None: cl.extend(CardEnc.atmost(lits,bound=hi,vpool=pool,encoding=EncType.seqcounter).clauses)
    if lo: cl.append(list(lits))
for v in range(P): card([x(v,t) for t in range(len(T))],1,1)
for v in range(k,P):
    for l in range(L):
        card([x(u,t) for u in range(v-k,v+1) for t,(S,ll) in enumerate(T) if ll==l and v-u in S],1,1)
    for d in range(1,k+1):
        lits=[x(u,t) for u in range(v-k,v-d+1) for t,(S,_) in enumerate(T) if v-d-u in S and v-u in S]
        card(lits,1,1 if w[d]>0 else None)
s=Cadical153(bootstrap_with=cl)
mid=range(c,c+k); states=[]; t0=time.time()
while s.solve():
    mod=set(l for l in s.get_model() if l>0)
    st=tuple(next(t for t in range(len(T)) if x(v,t) in mod) for v in mid)
    states.append(st); s.add_clause([-x(v,t) for v,t in zip(mid,st)])
    if len(states)%500==0: print(len(states),'states',round(time.time()-t0),'s',flush=True)
print('m',m,'P',P,'c',c,'states found',len(states),round(time.time()-t0),'s',flush=True)
pickle.dump(states,open('logs/satscan_m%d_P%d_c%d.pkl'%(m,P,c),'wb'))
S=set(states)
def okwin(win):   # local conditions at the last vertex of a (k+1)-window
    v=k
    for l in range(L):
        if sum(1 for j in range(k+1) if T[win[j]][1]==l and v-j in T[win[j]][0])!=1: return False
    for d in range(1,k+1):
        cnt=sum(1 for j in range(v-d+1) if v-d-j in T[win[j]][0] and v-j in T[win[j]][0])
        if cnt<1 or (w[d]>0 and cnt!=1): return False
    return True
byprefix=defaultdict(list)
for st in S: byprefix[st[:-1]].append(st)
edges={u:set() for u in S}
for u in S:
    for vv in byprefix.get(u[1:],()):
        if okwin(u+(vv[-1],)): edges[u].add(vv)
nodes=set(S)
while True:
    indeg=defaultdict(int)
    for u in nodes:
        edges[u]&=nodes
        for y in edges[u]: indeg[y]+=1
    keep={u for u in nodes if edges[u] and indeg[u]>0}
    if keep==nodes: break
    nodes=keep
# strongly connected components (Kosaraju)
order=[]; seen=set()
for s0 in nodes:
    if s0 in seen: continue
    seen.add(s0); stack=[(s0,iter(edges[s0]))]
    while stack:
        u,it=stack[-1]
        for y in it:
            if y not in seen: seen.add(y); stack.append((y,iter(edges[y]))); break
        else: stack.pop(); order.append(u)
radj=defaultdict(set)
for u in nodes:
    for y in edges[u]: radj[y].add(u)
comp={}
for s0 in reversed(order):
    if s0 in comp: continue
    comp[s0]=s0; stack=[s0]
    while stack:
        u=stack.pop()
        for y in radj[u]:
            if y not in comp: comp[y]=s0; stack.append(y)
groups=defaultdict(list)
for u,r in comp.items(): groups[r].append(u)
res=defaultdict(int)
for r,g in groups.items():
    gs=set(g)
    if len(g)==1 and g[0] not in edges[g[0]]: continue
    lev={g[0]:0}; q=[g[0]]; gg=0
    for u in q:
        for y in edges[u]:
            if y not in gs: continue
            if y not in lev: lev[y]=lev[u]+1; q.append(y)
            else: gg=math.gcd(gg,lev[u]+1-lev[y])
    res[gg]+=1
print('nodes after trim',len(nodes),'cyclic SCCs by period:',dict(res),flush=True)
