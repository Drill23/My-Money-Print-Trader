import numpy as np, pandas as pd, itertools, sys
sys.path.insert(0,'.')
from wick2 import sim2
df=pd.read_parquet('btc_all.parquet')
o,h,l,c=[df[x].values.astype(np.float64) for x in ['open','high','low','close']]
idx=df.index
c5=df.close.resample('5min').last(); r5=np.log(c5).diff()
sigd=(r5.rolling(288*7,min_periods=288*5).std()*np.sqrt(288)).shift(1).reindex(idx,method='ffill').values
np.save('sigd.npy',sigd)
cut=lambda d: int(np.searchsorted(idx.values,np.datetime64(d)))
pers={'A_19-22':(cut('2019-01-09'),cut('2023-01-01')),'B_23-24':(cut('2023-01-01'),cut('2025-01-01')),'C_25-26':(cut('2025-01-01'),len(df))}
rows=[]
for cyc,m,tp,sl,tmax in itertools.product([720,1440],[1.5,1.75,2.0,2.25,2.5,3.0],[0.5,0.75,1.0,1.25,1.5],[0,2.0,3.0,4.0],[720,1440,2880,4320]):
    d=dict(cyc=cyc,m=m,tp=tp,sl=sl,tmax=tmax)
    for p,(a,b) in pers.items():
        et,xt,r,w,wst=sim2(o,h,l,c,sigd,a,b,cyc,m,tp,sl,tmax,0.001,0.001)
        yrs=(b-a)/1440/365
        eq=np.cumprod(1+r); peak=np.maximum.accumulate(np.concatenate([[1],eq]))[:-1]
        mtm_dd=(1-(peak*0+np.concatenate([[1],eq])[:-1])*(1+wst)/peak).max() if len(r) else 0
        d[p+'_cagr']=((eq[-1] if len(r) else 1)**(1/yrs)-1)*100
        d[p+'_n']=len(r); d[p+'_win']=(r>0).mean()*100 if len(r) else 0; d[p+'_dd']=mtm_dd*100
    rows.append(d)
R=pd.DataFrame(rows); R.to_csv('sweep3.csv',index=False)
R['minc']=R[[p+'_cagr' for p in pers]].min(axis=1)
pd.set_option('display.width',250)
print(R.sort_values('minc',ascending=False).round(1).head(40).to_string(index=False))
print((R.minc>0).mean())
