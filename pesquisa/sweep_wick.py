import numpy as np, pandas as pd, itertools, sys
sys.path.insert(0,'.')
from wick import sim
df=pd.read_parquet('btc1m.parquet')
o,h,l,c=[df[x].values.astype(np.float64) for x in ['open','high','low','close']]
idx=df.index
c5=df.close.resample('5min').last(); r5=np.log(c5).diff()
# sigma de 24h (vol diaria) estimada com 7 dias anteriores
sigd=(r5.rolling(288*7).std()*np.sqrt(288)).shift(1).reindex(idx,method='ffill').values
split=np.searchsorted(idx.values, np.datetime64('2025-01-01'))
st=1440*8; end=len(df)
rows=[]
for cyc,m,tp,sl,tmax in itertools.product([720,1440],[0.75,1.0,1.25,1.5,2.0,2.5],[0.5,0.75,1.0,1.5],[0,1.0,1.5,2.5],[0,1440,2880]):
    for per,(a,b) in [('IS',(st,split)),('OOS',(split,end))]:
        et,xt,r,w,eq=sim(o,h,l,c,sigd,a,b,cyc,m,tp,sl,tmax,0.001,0.001,1.0)
        days=(b-a)/1440
        rows.append(dict(cyc=cyc,m=m,tp=tp,sl=sl,tmax=tmax,per=per,n=len(r),avg=r.mean()*100 if len(r) else 0,
            win=(r>0).mean()*100 if len(r) else 0,tot=(np.prod(1+r)-1)*100,
            mdd=(1-(np.cumprod(1+r)/np.maximum.accumulate(np.cumprod(1+r)))).max()*100 if len(r) else 0,
            inmkt=((xt-et).sum()/(b-a))*100))
R=pd.DataFrame(rows); R.to_csv('sweep_wick.csv',index=False)
P=R.pivot_table(index=['cyc','m','tp','sl','tmax'],columns='per',values=['n','avg','win','tot','mdd','inmkt'])
P.columns=[x+'_'+y for x,y in P.columns]
pd.set_option('display.width',250)
P['score']=np.minimum(P.tot_IS,P.tot_OOS)
print(P.sort_values('score',ascending=False).round(2).head(30).to_string())
print('BTC hold IS %.1f%% OOS %.1f%%'%((c[split-1]/o[st]-1)*100,(c[-1]/o[split]-1)*100))
