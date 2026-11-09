import pandas as pd,numpy as np,pyreadr,json,collections,sys
from scipy import stats
df=pd.read_pickle('/tmp/claude-0/w17/sel197.pkl').reset_index(drop=True)
txt=(df['TI'].fillna('')+' '+df['AB'].fillna('')+' '+df['DE'].fillna('')).str.lower()
flag=~txt.str.contains(r'pick|arrival|onset|phase')
named=df.TI.str.contains('INTELLIGENT REAL-TIME EARTHQUAKE DETECTION BY RECURRENT|SEISMOGEN:',regex=True)
B=flag|named
G={}
for name,f in [('G1','Group1-Models.RData'),('G2','Group2-Aplications.RData'),('G3','Group3-Datasets.RData'),('G4','Group4-TL-SD.RData')]:
    d=list(pyreadr.read_r('/tmp/supp/Data/'+f).values())[0]; dois=set(d.DI.dropna().str.lower())
    G[name]=df.DI.str.lower().isin(dois)
grp=pd.Series('',index=df.index)
for k,m in G.items(): grp[m]=k
print('boundary per group', grp[B].value_counts().to_dict(), 'total',int(B.sum()))
for i,r in df[B].iterrows(): print('  ',grp[i],r.AU.split(';')[0].split(',')[0],int(r.PY),r.TI[:70])
def ind(d,g):
    n=len(d); ann=d.PY.astype(int).value_counts().sort_index()
    cagr=((ann[2025]/ann[2020])**(1/5)-1)*100
    b=np.polyfit(ann.index.values-2020,np.log(ann.values),1); rate=(np.exp(b[0])-1)*100
    tc=np.sort(d.TC.values); gi=(2*np.arange(1,n+1)-n-1).dot(tc)/(n*tc.sum())
    au=[a for s in d.AU for a in set(x.strip() for x in s.split(';') if x.strip())]
    c=collections.Counter(au); dist=collections.Counter(c.values()); x=np.array(sorted(dist)); f=np.array([dist[k] for k in x])
    bb=np.polyfit(np.log(x),np.log(f/f.sum()),1)
    tcpy=d.TC/(2026-d.PY.astype(int)+1)
    g3=tcpy[g=='G3'].values; rest=np.concatenate([tcpy[g==k].values for k in ('G1','G2','G4')])
    u=stats.mannwhitneyu(g3,rest,alternative='two-sided',method='asymptotic'); rb=2*u.statistic/(len(g3)*len(rest))-1
    rng=np.random.default_rng(1); allv=np.concatenate([g3,rest]); cnt=0;R=20000
    for _ in range(R):
        p=rng.permutation(allv); Up=stats.mannwhitneyu(p[:len(g3)],p[len(g3):],alternative='two-sided').statistic
        if abs(Up-len(g3)*len(rest)/2)>=abs(u.statistic-len(g3)*len(rest)/2): cnt+=1
    return dict(n=n,groups={k:int((g==k).sum()) for k in ['G1','G2','G3','G4']},cagr=round(cagr,1),exp=round(rate,1),gini=round(gi,3),lotka=round(-bb[0],2),once=round(100*dist[1]/sum(dist.values()),1),authors=len(c),
                med={k:round(float(np.median(tcpy[g==k])),2) for k in ['G1','G2','G3','G4']},U=float(u.statistic),p=round(float(u.pvalue),3),pperm=round((cnt+1)/(R+1),3),rb=round(float(rb),2),g3=sorted(np.round(g3,2).tolist()))
full=ind(df,grp); sens=ind(df[~B],grp[~B])
print(json.dumps(full)); print(json.dumps(sens))
json.dump({'rule':'boundary = no match of pick|arrival|onset|phase in title, abstract or author keywords, plus reviewer-named Chin 2020 and Wang 2021 (SeismoGen)','boundary':[{'group':grp[i],'first_author':r.AU.split(';')[0],'PY':int(r.PY),'TI':r.TI,'DI':r.DI,'reason':'reviewer-named' if named[i] else 'no pick/arrival/onset/phase term'} for i,r in df[B].iterrows()],'full':full,'without_boundary':sens},open('/tmp/claude-0/w18/boundary_sensitivity.json','w'),indent=1)
