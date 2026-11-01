import numpy as np, pandas as pd, itertools, sys
sys.path.insert(0,'.')
from engine import run_grid, load
df=load()
o,h,l,c=[df[x].values.astype(np.float64) for x in ['open','high','low','close']]
idx=df.index
c5=df.close.resample('5min').last(); r5=np.log(c5).diff()
sig=(r5.rolling(288).std()*np.sqrt(144)).reindex(idx,method='ffill').values
N12=720
starts=np.arange(1440*2, len(df)-N12, 240); yrs=idx[starts].year
hold=np.array([c[s+N12-1]/o[s]-1 for s in starts])
for fee in [0.0,0.0005,0.00075,0.001]:
  for k,N in [(1.0,4),(1.5,4),(2.0,4),(2.0,8),(3.0,6),(3.0,12),(1.0,8)]:
    res=[];
    for s in starts:
        p=o[s]; w=k*sig[s]
        mtm,liq,ntr,why,_,b,qq=run_grid(o,h,l,c,s,N12,p*np.exp(-w),p*np.exp(w),N,fee,fee,0.0,0.0,1.0)
        res.append(mtm-1)
    res=np.array(res)
    # regressao: ret = a + beta*hold  -> 'a' = alfa de grid descontada exposicao
    out=[]
    for per,m in [('IS',yrs<=2024),('OOS',yrs>=2025)]:
        x=res[m]; y=hold[m]; beta=np.cov(x,y)[0,1]/y.var(); a=x.mean()-beta*y.mean()
        out.append(f"{per}: mean {x.mean()*100:+.3f}% alpha {a*100:+.3f}% beta {beta:.2f} win {(x>0).mean()*100:.0f}%")
    print(f"fee {fee*100:.3f}% k={k} N={N} sp={np.mean(np.exp(2*k*sig[starts]/N)-1)*100:.2f}% | "+' | '.join(out))
