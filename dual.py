"""LP: max sum_d y_d s.t. for every set S inside a window {0..k} (containing 0): sum_{pairs} y_{dist} <= |S|."""
import sys, itertools, numpy as np
from scipy.optimize import linprog
from fractions import Fraction
k=int(sys.argv[1])
rows=[];b=[]
for mask in range(1<<k):
    S=[0]+[i+1 for i in range(k) if mask>>i&1]
    if len(S)<2: continue
    r=np.zeros(k)
    for x,y in itertools.combinations(S,2): r[y-x-1]+=1
    rows.append(r); b.append(len(S))
res=linprog(-np.ones(k),A_ub=np.array(rows),b_ub=np.array(b),bounds=[(0,None)]*k,method='highs')
print('k=%d LP=%.6f'%(k,-res.fun)); print('y=',[str(Fraction(v).limit_denominator(100)) for v in res.x])
