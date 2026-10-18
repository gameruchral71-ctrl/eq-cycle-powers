import sys
sys.path.insert(0,'/mnt/project-files/eq-cycle-powers')
from structure import all_solutions, classes, is_tiling
n,k,t=24,7,4
sols=all_solutions(n,k,t)
done=0
for sol in sols:
    if not any(is_tiling(n,k,L) for L in sol):
        for L in sol:
            cs=sorted(classes(n,L),key=min)
            print(' '.join('{'+','.join(map(str,c))+'}' for c in cs if len(c)>1))
        print(); done+=1
        if done==2: break
sol=[s for s in sols if any(is_tiling(n,k,L) for L in s)][0]
for L in sol:
    cs=sorted(classes(n,L),key=min); print(' '.join('{'+','.join(map(str,c))+'}' for c in cs if len(c)>1))
