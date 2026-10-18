import itertools
def weights(m):
    N=2**m; w={d:0 for d in range(1,N)}
    for j in range(1,m): w[N-2**j]=1
    w[N-1]=2
    return w
def tight_sets(m):
    N=2**m; k=N-1; w=weights(m); out=[]
    for mask in range(1<<(k-1)):
        S=[0]+[i+1 for i in range(k-1) if mask>>i&1]+[k]
        W=sum(w[y-x] for x,y in itertools.combinations(S,2))
        if W==len(S): out.append(tuple(S))
    return out
if __name__=='__main__':
    for m in (2,3,4):
        N=2**m; T=tight_sets(m); h=N//2
        L=sorted({tuple(x for x in S if x<h) for S in T}); R=sorted({tuple(x for x in S if x>=h) for S in T})
        prod= len(L)*len(R)==len(T)
        print(m,len(T),len(L),len(R),'product' if prod else 'not product')
        if m==3: print('L',L); print('R',R)
