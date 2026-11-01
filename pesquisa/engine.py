import numpy as np, pandas as pd
from numba import njit

@njit(cache=True)
def run_grid(o,h,l,c, s, n_min, lower, upper, N, fee, fee_taker, sl, tp, inv):
    """Simula um Spot Grid geometrico da Binance em candles de 1m.
    s: indice inicial; n_min: duracao em minutos. Retorna (valor_final_mtm, valor_final_liquidado,
    n_trades, motivo_fim(0=tempo,1=SL,2=TP), minutos_ativos, base_final, quote_final)"""
    r = (upper/lower)**(1.0/N)
    lv = np.empty(N+1)
    for i in range(N+1): lv[i] = lower*r**i
    q = inv/N
    p0 = o[s]
    hold = np.zeros(N, np.int8)   # 1 = celula com moeda (espera vender em lv[j+1]); 0 = com USDT/BRL (espera comprar em lv[j])
    base = np.zeros(N)
    quote = 0.0
    trades = 0
    # abertura: celulas totalmente acima do preco compram moeda a mercado (taker)
    for j in range(N):
        if lv[j] > p0:
            hold[j] = 1; base[j] = q/p0*(1-fee_taker); trades += 1
        else:
            hold[j] = 0
    cash = 0.0  # lucro realizado + sobras
    qc = np.full(N, q)
    for j in range(N):
        if hold[j]==1: qc[j]=0.0
    path = np.empty(4)
    for t in range(s, s+n_min):
        if c[t] >= o[t]:
            path[0]=o[t]; path[1]=l[t]; path[2]=h[t]; path[3]=c[t]
        else:
            path[0]=o[t]; path[1]=h[t]; path[2]=l[t]; path[3]=c[t]
        for k in range(3):
            a = path[k]; b = path[k+1]
            if b > a:
                if tp > 0 and b >= tp:
                    # vende tudo no TP
                    tot = cash
                    for j in range(N): tot += qc[j] + base[j]*tp*(1-fee_taker)
                    return tot, tot, trades, 2, t-s+1, 0.0, tot
                for j in range(N):
                    if hold[j]==1 and lv[j+1] > a and lv[j+1] <= b:
                        proceeds = base[j]*lv[j+1]*(1-fee)
                        cash += proceeds - q  # lucro realizado separado
                        qc[j] = q; base[j] = 0.0; hold[j] = 0; trades += 1
            elif b < a:
                if sl > 0 and b <= sl:
                    tot = cash
                    for j in range(N): tot += qc[j] + base[j]*sl*(1-fee_taker)
                    return tot, tot, trades, 1, t-s+1, 0.0, tot
                for j in range(N):
                    if hold[j]==0 and lv[j] < a and lv[j] >= b:
                        base[j] = qc[j]/lv[j]*(1-fee); qc[j] = 0.0; hold[j] = 1; trades += 1
    pe = c[s+n_min-1]
    b_tot = 0.0; q_tot = cash
    for j in range(N): b_tot += base[j]; q_tot += qc[j]
    mtm = q_tot + b_tot*pe
    liq = q_tot + b_tot*pe*(1-fee_taker)
    return mtm, liq, trades, 0, n_min, b_tot, q_tot

def load():
    import os
    df = pd.read_parquet(os.path.join(os.path.dirname(__file__),'btc1m.parquet'))
    return df
