import numpy as np
from numba import njit
@njit(cache=True)
def sim2(o,h,l,c,sig,start,end,cycle,m,tp,sl,tmax,fee_m,fee_t):
    nmax=50000
    ent=np.zeros(nmax,np.int64); ex=np.zeros(nmax,np.int64); ret=np.zeros(nmax); why=np.zeros(nmax,np.int8); worst=np.zeros(nmax)
    n=0; t=start
    while t<end:
        s=sig[t]
        if not (s>0): t+=cycle; continue
        lim=o[t]*(1-m*s); filled=-1
        for u in range(t,min(t+cycle,end)):
            if l[u]<=lim*(1-1e-4): filled=u; break
        if filled<0: t+=cycle; continue
        px=lim; tpp=px*(1+tp*s); slp=px*(1-sl*s) if sl>0 else 0.0
        w=0; xp=0.0; u=filled; mn=l[filled]
        if sl>0 and l[filled]<=slp: w=1; xp=slp
        else:
            u=filled+1
            while u<end:
                if l[u]<mn: mn=l[u]
                if sl>0 and l[u]<=slp: w=1; xp=min(slp,o[u]); break
                if h[u]>=tpp: w=2; xp=tpp if o[u]<tpp else o[u]; break
                if tmax>0 and u-filled>=tmax: w=3; xp=c[u]; break
                u+=1
            if w==0: w=4; u=end-1; xp=c[u]
        fe=fee_m if w==2 else fee_t
        ret[n]=xp*(1-fe)/(px/(1-fee_m))-1; worst[n]=mn/px-1
        ent[n]=filled; ex[n]=u; why[n]=w; n+=1
        t=u+1
    return ent[:n],ex[:n],ret[:n],why[:n],worst[:n]
