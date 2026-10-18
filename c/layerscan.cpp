// C++ version of layerscan.py: enumerate valid (k+1)-windows of (tight set, layer) types,
// print each window as a line of type indices (to be post-processed in Python).
#include <bits/stdc++.h>
using namespace std;
int m,N,k,L; vector<int> w; vector<vector<int>> TS; vector<int> Tl; vector<int> Tset;
int cov[8][64]; int pc[64][64]; int win[64]; long long nwin=0; FILE* out;
bool okadd(int t,int j){const auto&S=TS[Tset[t]];int l=Tl[t];
 for(int s:S) if(cov[l][j+s]) return false;
 for(size_t a=0;a<S.size();a++)for(size_t b=a+1;b<S.size();b++) if(w[S[b]-S[a]]>0&&pc[j+S[a]][j+S[b]]) return false; return true;}
void add(int t,int j,int sg){const auto&S=TS[Tset[t]];int l=Tl[t];
 for(int s:S) cov[l][j+s]+=sg;
 for(size_t a=0;a<S.size();a++)for(size_t b=a+1;b<S.size();b++) if(w[S[b]-S[a]]>0) pc[j+S[a]][j+S[b]]+=sg;}
vector<vector<char>> mem;
bool final_(){int v=k; for(int l=0;l<L;l++) if(cov[l][v]!=1) return false;
 for(int d=1;d<=k;d++){bool f=false; for(int j=0;j<=v-d&&!f;j++){auto&M=mem[Tset[win[j]]]; if(M[v-d-j]&&M[v-j]) f=true;} if(!f) return false;} return true;}
// extra pruning: vertex x=j-1 (all classes containing x have left end <= x <= j-1 ... only if window covers x-k..x) skip
void rec(int j){ if(j==k+1){ if(final_()){nwin++; for(int i=0;i<=k;i++) fprintf(out,"%d ",win[i]); fprintf(out,"\n");} return;}
 for(int t=0;t<(int)Tl.size();t++) if(okadd(t,j)){add(t,j,1);win[j]=t;rec(j+1);add(t,j,-1);} }
int main(int argc,char**argv){m=atoi(argv[1]);N=1<<m;k=N-1;L=m+1;w.assign(N,0);for(int j=1;j<m;j++)w[N-(1<<j)]=1;w[N-1]=2;
 for(int mask=0;mask<(1<<(k-1));mask++){vector<int>S{0};for(int i=0;i<k-1;i++)if(mask>>i&1)S.push_back(i+1);S.push_back(k);
  int W=0;for(size_t a=0;a<S.size();a++)for(size_t b=a+1;b<S.size();b++)W+=w[S[b]-S[a]]; if(W==(int)S.size()) TS.push_back(S);}
 for(size_t s=0;s<TS.size();s++){vector<char>M(N,0);for(int x:TS[s])M[x]=1;mem.push_back(M);for(int l=0;l<L;l++){Tset.push_back(s);Tl.push_back(l);}}
 out=fopen(argv[2],"w"); fprintf(stderr,"types %zu\n",Tl.size()); rec(0); fclose(out); fprintf(stderr,"windows %lld\n",nwin);}
