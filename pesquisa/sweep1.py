import numpy as np, pandas as pd, itertools, sys
sys.path.insert(0,'.')
from engine import run_grid, load
df=load()
o,h,l,c=[df[x].values.astype(np.float64) for x in ['open','high','low','close']]
idx=df.index
lc=np.log(df.close.values)
# vol de 12h estimada pelas 24h anteriores (retornos de 5m)
c5=df.close.resample('5min').last()
r5=np.log(c5).diff()
sig5=r5.rolling(288).std()*np.sqrt(144)   # sigma 12h
sig=sig5.reindex(idx,method='ffill').values
N12=720
starts=[i for i in range(1440*2, len(df)-N12, 240) ]
starts=np.array(starts)
yrs=idx[starts].year
FEE=0.001
rows=[]
for k,N,slk in itertools.product([0.75,1.0,1.5,2.0,2.5,3.0,4.0],[3,4,5,6,8,10,15,20],[0,0.5,1.0]):
    res=np.empty(len(starts)); ends=np.empty(len(starts)); tr=np.empty(len(starts))
    for n,s in enumerate(starts):
        p=o[s]; w=k*sig[s]
        lower=p*np.exp(-w); upper=p*np.exp(w)
        sl = lower*np.exp(-slk*sig[s]) if slk>0 else 0.0
        mtm,liq,ntr,why,_,_,_=run_grid(o,h,l,c,s,N12,lower,upper,N,FEE,FEE,sl,0.0,1.0)
        res[n]=liq-1; ends[n]=why; tr[n]=ntr
    spacing=np.mean((np.exp(2*k*sig[starts]/N)-1))
    for per,m in [('IS',yrs<=2024),('OOS',yrs>=2025)]:
        x=res[m]
        rows.append(dict(k=k,N=N,slk=slk,per=per,spacing=spacing*100,mean=x.mean()*100,med=np.median(x)*100,win=(x>0).mean()*100,p5=np.percentile(x,5)*100,trades=tr[m].mean(),slhit=(ends[m]==1).mean()*100))
R=pd.DataFrame(rows)
R.to_csv('sweep1.csv',index=False)
hold=np.array([c[s+N12-1]/o[s]-1 for s in starts])
for per,m in [('IS',yrs<=2024),('OOS',yrs>=2025)]:
    x=hold[m]*100; print(per,'HOLD mean %.3f med %.3f win %.1f p5 %.2f n=%d'%(x.mean(),np.median(x),(x>0).mean()*100,np.percentile(x,5),m.sum()))
P=R.pivot_table(index=['k','N','slk'],columns='per',values=['mean','win','p5','spacing'])
P.columns=[a+'_'+b for a,b in P.columns]
P=P.sort_values('mean_IS',ascending=False)
pd.set_option('display.width',200)
print(P.round(3).head(25).to_string())
print('--- top by OOS')
print(P.sort_values('mean_OOS',ascending=False).round(3).head(15).to_string())
