import sys
sys.path.insert(0,'/mnt/project-files/eq-cycle-powers')
from structure import all_solutions, classes
def positions(n,k,layer):
    pos={}
    for C in classes(n,layer):
        # find left endpoint a: the element a such that all others are within a..a+k (cyclically)
        for a in C:
            if all((x-a)%n<=k for x in C): break
        for x in C: pos[x]=(x-a)%n
    return pos
for (n,k,t) in [(8,3,3),(12,3,3),(16,3,3),(16,7,4),(24,7,4)]:
    sols=all_solutions(n,k,t,limit=3000)
    N=k+1
    stats={}
    for sol in sols:
        P=[positions(n,k,L) for L in sol]
        diffs=[ (sum(p[(v+1)%n] for p in P)-sum(p[v] for p in P))%N for v in range(n)]
        stats.setdefault(tuple(sorted(set(diffs))),0); stats[tuple(sorted(set(diffs)))]+=1
    print(n,k,len(sols),stats)
