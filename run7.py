import sys,time
from eqsat import solve
k=int(sys.argv[1]); t=int(sys.argv[2])
for n in map(int,sys.argv[3:]):
    t0=time.time(); r,_=solve(n,k,t); print('k=%d n=%d t=%d %s %.1fs'%(k,n,t,'SAT' if r else 'UNSAT',time.time()-t0),flush=True)
