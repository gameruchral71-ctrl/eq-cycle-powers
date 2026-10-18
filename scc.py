"""Read valid windows (one per line, k+1 type ids) from c/layerscan output; build the de Bruijn graph
(states = k consecutive types), trim, and print each strongly connected component's period
(gcd of its cycle lengths). Every closed walk lies in one SCC, so its length is a multiple of that period."""
import sys, math
from collections import defaultdict
ids={}; edges=defaultdict(set)
def nid(x):
    if x not in ids: ids[x]=len(ids)
    return ids[x]
for line in open(sys.argv[1]):
    t=tuple(map(int,line.split()))
    edges[nid(t[:-1])].add(nid(t[1:]))
nodes=set(range(len(ids)))
while True:
    indeg=defaultdict(int)
    for u in nodes:
        edges[u]&=nodes
        for x in edges[u]: indeg[x]+=1
    keep={u for u in nodes if edges[u] and indeg[u]>0}
    if keep==nodes: break
    nodes=keep
print('states',len(ids),'after trim',len(nodes),flush=True)
index={};low={};onst=set();st=[];comps=[];c=[0]
for v0 in nodes:
    if v0 in index: continue
    stack=[(v0,iter(edges[v0]))]; index[v0]=low[v0]=c[0]; c[0]+=1; st.append(v0); onst.add(v0)
    while stack:
        u,itr=stack[-1]
        for x in itr:
            if x not in index:
                index[x]=low[x]=c[0]; c[0]+=1; st.append(x); onst.add(x); stack.append((x,iter(edges[x]))); break
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
periods=defaultdict(int)
for comp in comps:
    cs=set(comp)
    if len(comp)==1 and comp[0] not in edges[comp[0]]: continue
    lev={comp[0]:0}; q=[comp[0]]; g=0
    for u in q:
        for x in edges[u]:
            if x not in cs: continue
            if x not in lev: lev[x]=lev[u]+1; q.append(x)
            else: g=math.gcd(g,lev[u]+1-lev[x])
    periods[g]+=1
print('cyclic SCCs by period:',dict(periods))
