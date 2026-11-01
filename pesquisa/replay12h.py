"""Simulacao 'ao vivo' de 12h: percorre minuto a minuto, a estrategia so enxerga dados passados."""
import pandas as pd, numpy as np, sys
df=pd.read_parquet('btc_all.parquet')
FEE=0.001; STOP=0.25
def sinal(closes_diarios):
    d=closes_diarios; c=d.iloc[-1]
    v=[c>d.iloc[-30:].mean(), c>d.iloc[-50:].mean(), c>d.iloc[-100:].mean(), c>d.iloc[-15], c>d.iloc[-29], c>d.iloc[-57]]
    return int(sum(v)), v
def replay(t0, saldo=50.0, verbose=True):
    t0=pd.Timestamp(t0); t1=t0+pd.Timedelta(hours=12)
    hist=df.loc[:t0-pd.Timedelta(minutes=1)]
    daily=hist.close.resample('1D').last()
    # o candle diario so 'fecha' a 00:00 UTC: usa apenas dias completos
    daily=daily[daily.index < t0.normalize()]
    soma,v=sinal(daily); pos = soma>=3
    caixa=saldo; btc=0.0; log=[]
    p0=df.open.loc[t0]
    if pos:
        btc=caixa/p0*(1-FEE); caixa=0.0; stop=daily.iloc[-1]*(1-STOP)
        log.append(f"{t0} sinal {soma}/6 -> COMPRA {btc:.8f} BTC a {p0:.2f}; stop de seguranca {stop:.2f}")
    else:
        stop=None; log.append(f"{t0} sinal {soma}/6 -> FICA EM CAIXA (tendencia negativa)")
    w=df.loc[t0:t1-pd.Timedelta(minutes=1)]
    minval=saldo; maxval=saldo
    for ts,row in w.iterrows():
        if ts.hour==0 and ts.minute==0 and ts!=t0:
            daily2=df.loc[:ts-pd.Timedelta(minutes=1)].close.resample('1D').last()
            soma,v=sinal(daily2); novo=soma>=3
            if novo and btc==0: btc=caixa/row.open*(1-FEE); caixa=0; log.append(f"{ts} sinal {soma}/6 -> COMPRA a {row.open:.2f}")
            elif not novo and btc>0: caixa=btc*row.open*(1-FEE); btc=0; log.append(f"{ts} sinal {soma}/6 -> VENDE a {row.open:.2f}")
            else: log.append(f"{ts} fechamento diario: sinal {soma}/6 -> mantem")
        if btc>0 and stop and row.low<=stop:
            caixa=btc*stop*(1-FEE)*(1-0.002); btc=0; log.append(f"{ts} STOP de seguranca executado")
        val=caixa+btc*row.close; minval=min(minval,caixa+btc*row.low); maxval=max(maxval,caixa+btc*row.high)
    final=caixa+btc*w.close.iloc[-1]*(1-FEE)  # liquidando ao fim do teste
    btcmov=w.close.iloc[-1]/p0-1
    if verbose:
        print('\n'.join(log))
        print(f"BTC nas 12h: {p0:.2f} -> {w.close.iloc[-1]:.2f} ({btcmov*100:+.2f}%)")
        print(f"Saldo: R$ {saldo:.2f} -> R$ {final:.2f} ({(final/saldo-1)*100:+.2f}%) | min R$ {minval:.2f} max R$ {maxval:.2f}")
    return final, btcmov, pos
if __name__=='__main__':
    replay(sys.argv[1] if len(sys.argv)>1 else '2026-10-24 12:00')
