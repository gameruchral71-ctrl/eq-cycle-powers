import sys
sys.path.insert(0,'/mnt/project-files/eq-cycle-powers')
from structure import all_solutions, classes
from collections import Counter
def norm(n,k,C):
    for a in C:
        if all((x-a)%n<=k for x in C): return tuple(sorted((x-a)%n for x in C))
for n in map(int,sys.argv[2:]):
    k=int(sys.argv[1])
    sols=all_solutions(n,k,k.bit_length()+1,limit=int(__import__("os").environ.get("LIM","5000")))
    c=Counter()
    for sol in sols:
        for L in sol:
            for C in classes(n,L): c[norm(n,k,C)]+=1
    print(n,len(sols),sorted(c.items(),key=lambda x:-x[1]))
