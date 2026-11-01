import numpy as np, pandas as pd
from numba import njit

@njit(cache=True)
def sim(o,h,l,c, sig, start, end, cycle, m, tp, sl, tmax, fee_m, fee_t, frac):
    """Pega-pavio: a cada 'cycle' minutos (sem posicao), coloca compra limite em P*(1-m*sig).
    Se executar: OCO com TP (limite, maker) em +tp*sig_entry? -> aqui tp/sl em multiplos de sig tambem.
    tmax: saida por tempo (minutos, 0=sem). Retorna arrays de trades."""
    eq=1.0
    nmax=20000
    ent_t=np.zeros(nmax,np.int64); ex_t=np.zeros(nmax,np.int64); ret=np.zeros(nmax); why=np.zeros(nmax,np.int8)
    eqc=np.zeros(nmax)
    n=0
    t=start
    while t < end:
        s=sig[t]
        if not (s>0):
            t+=cycle; continue
        lim=o[t]*(1-m*s)
        filled=-1
        for u in range(t, min(t+cycle,end)):
            if l[u] <= lim*(1-1e-4):
                filled=u; break
        if filled<0:
            t+=cycle; continue
        # posicao aberta
        px=lim
        tpp=px*(1+tp*s); slp=px*(1-sl*s) if sl>0 else 0.0
        # verifica no proprio minuto da entrada apenas SL (conservador)
        exit_px=0.0; w=0; u=filled
        if sl>0 and l[filled] <= slp:
            exit_px=slp; w=1
        else:
            u=filled+1
            while u<end:
                if sl>0 and l[u]<=slp:
                    exit_px=min(slp,o[u]); w=1; break
                if h[u]>=tpp:
                    exit_px=max(tpp,o[u]) if o[u]>tpp else tpp; w=2; break
                if tmax>0 and u-filled>=tmax:
                    exit_px=c[u]; w=3; break
                u+=1
            if w==0:
                exit_px=c[end-1]; u=end-1; w=4
        fe = fee_m if w==2 else fee_t
        r=(exit_px*(1-fe))/(px/(1-fee_m)) - 1  # entrada maker
        eq*=1+frac*r
        ent_t[n]=filled; ex_t[n]=u; ret[n]=r; why[n]=w; eqc[n]=eq; n+=1
        t=u+1
    return ent_t[:n],ex_t[:n],ret[:n],why[:n],eqc[:n]
