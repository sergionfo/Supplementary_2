import pandas as pd, numpy as np, collections, json, re, pyreadr
from scipy import stats
df0=pd.read_pickle('/tmp/claude-0/work/sel.pkl')
bad=df0.DI.str.lower()=='10.5194/nhess-21-339-2021'
df=df0[~bad].copy(); df.to_pickle('sel197.pkl')
try: pyreadr.write_rdata('Selected_Pub_197.RData', df.reset_index(drop=True).astype(str), df_name='M')
except Exception as e: print('rdata',e)
M={}
n=len(df); M['n']=n
so=df.SO.str.replace(' AND ',' & ')
M['sources_raw']=int(df.SO.nunique()); M['sources_merged']=int(so.nunique())
au=[a.strip() for s in df.AU.dropna() for a in s.split(';') if a.strip()]
M['authors']=len(set(au)); M['author_appearances']=len(au); M['coauth_per_doc']=round(len(au)/n,2)
M['single_auth_docs']=int(sum(1 for s in df.AU if len([a for a in s.split(';') if a.strip()])==1))
y=df.PY.astype(int).value_counts().sort_index(); M['annual']=y.to_dict()
M['cagr']=round(((y[2025]/y[2020])**(1/5)-1)*100,1)
M['avg_age']=round((2026-df.PY.astype(int)).mean(),2)
M['avg_cit']=round(df.TC.mean(),2); M['tc_total']=int(df.TC.sum())
cr=set(x.strip() for s in df.CR.dropna() for x in s.split(';') if x.strip()); M['refs']=len(cr)
cr0=set(x.strip() for s in df0.CR.dropna() for x in s.split(';') if x.strip()); M['refs198_check']=len(cr0)
de=set(k.strip().lower() for s in df.DE.dropna() for k in s.split(';') if k.strip()); idk=set(k.strip().lower() for s in df.ID.dropna() for k in s.split(';') if k.strip())
de0=set(k.strip().lower() for s in df0.DE.dropna() for k in s.split(';') if k.strip()); id0=set(k.strip().lower() for s in df0.ID.dropna() for k in s.split(';') if k.strip())
M['DE']=len(de); M['ID']=len(idk); M['DE198']=len(de0); M['ID198']=len(id0)
# international coauthorship from C1 countries
def countries(c1):
    out=set()
    for a in str(c1).split(';'):
        a=a.strip().rstrip('.')
        if not a: continue
        last=a.split(',')[-1].strip()
        if 'USA' in last or re.search(r'\b[A-Z]{2} \d{5}',last): last='USA'
        if 'PEOPLES R CHINA' in last or last=='CHINA': last='CHINA'
        out.add(last)
    return out
mcp=[len(countries(c))>1 for c in df.C1]; M['intl_pct']=round(100*sum(mcp)/n,2)
mcp0=[len(countries(c))>1 for c in df0.C1]; M['intl_pct198_check']=round(100*sum(mcp0)/len(df0),2)
# exponential fit
t=np.array(sorted(y.index))-2020; b=np.polyfit(t,np.log(y.values),1); pred=np.polyval(b,t)
M['exp_rate']=round((np.exp(b[0])-1)*100,1); M['exp_r2']=round(1-((np.log(y.values)-pred)**2).sum()/((np.log(y.values)-np.log(y.values).mean())**2).sum(),2); M['doubling']=round(np.log(2)/b[0],2)
# Lotka
c=collections.Counter(au); dist=collections.Counter(c.values()); x=np.array(sorted(dist)); f=np.array([dist[k] for k in x])
bb=np.polyfit(np.log(x),np.log(f/f.sum()),1); M['lotka_beta']=round(-bb[0],2); M['lotka_once']=round(100*dist[1]/sum(dist.values()),1); M['lotka']=sorted(dist.items())
# Bradford
sc=so.value_counts(); cum=sc.cumsum(); tot=sc.sum(); z=np.where(cum<=tot/3,1,np.where(cum<=2*tot/3,2,3))
M['bradford']={k:{'sources':int((z==k).sum()),'articles':int(sc[z==k].sum())} for k in (1,2,3)}; M['core_share']=round(100*sc[z==1].sum()/tot,1)
# Gini
tc=np.sort(df.TC.values); k=np.arange(1,n+1); g=lambda v:(2*np.arange(1,len(v)+1)-len(v)-1).dot(np.sort(v))/(len(v)*np.sort(v).sum())
M['gini']=round(g(tc),3); M['gini_wo_eqt']=round(g(tc[:-1]),3); M['top10_share']=round(100*np.sort(df.TC.values)[::-1][:10].sum()/tc.sum(),1); M['top1_share']=round(100*tc[-1]/tc.sum(),1); M['uncited']=int((tc==0).sum())
M['lorenz']=[[i/n,float(np.concatenate([[0],np.cumsum(tc)/tc.sum()])[i])] for i in range(0,n+1)]
# normalized TC (Bibliometrix: TC / mean TC of same-year docs)
yrmean=df.groupby('PY').TC.mean(); df['NTC']=df.TC/df.PY.map(yrmean); df['TCpY']=df.TC/(2026-df.PY.astype(int))
top=df.sort_values('TC',ascending=False).head(10)
M['top10']=[[r.AU.split(';')[0].split(',')[0].title(),int(r.PY),int(r.TC),round(r.TC/(2026-int(r.PY)+1),2),round(r.NTC,2),r.DI] for _,r in top.iterrows()]
# groups
G={}
for name,f in [('G1','Group1-Models.RData'),('G2','Group2-Aplications.RData'),('G3','Group3-Datasets.RData'),('G4','Group4-TL-SD.RData')]:
    d=list(pyreadr.read_r('/tmp/supp/Data/'+f).values())[0]; dois=set(d.DI.dropna().str.lower())
    G[name]=df[df.DI.str.lower().isin(dois)]
M['groups_n']={k:len(v) for k,v in G.items()}
tcpy=lambda d:(d.TC/(2026-d.PY.astype(int)+1)).values
g3=tcpy(G['G3']); rest=np.concatenate([tcpy(G[k]) for k in ('G1','G2','G4')])
M['tcpy_median']={k:round(float(np.median(tcpy(v))),2) for k,v in G.items()}
M['tcpy_iqr']={k:[round(float(np.percentile(tcpy(v),25)),2),round(float(np.percentile(tcpy(v),75)),2)] for k,v in G.items()}
u1=stats.mannwhitneyu(g3,rest,alternative='greater',method='asymptotic'); u2=stats.mannwhitneyu(g3,rest,alternative='two-sided',method='asymptotic')
u2e=stats.mannwhitneyu(g3,rest,alternative='two-sided',method='exact') if False else None
rb=2*u2.statistic/(len(g3)*len(rest))-1
# permutation exact-ish p
rng=np.random.default_rng(1); allv=np.concatenate([g3,rest]); obs=np.median(g3)-np.median(rest)
U_obs=u2.statistic; cnt=0; R=20000
for _ in range(R):
    p=rng.permutation(allv); Up=stats.mannwhitneyu(p[:len(g3)],p[len(g3):],alternative='two-sided').statistic
    if abs(Up-len(g3)*len(rest)/2)>=abs(U_obs-len(g3)*len(rest)/2): cnt+=1
M['mw']={'n1':len(g3),'n2':len(rest),'U':float(u2.statistic),'p_one':round(float(u1.pvalue),4),'p_two':round(float(u2.pvalue),4),'p_perm_two':round((cnt+1)/(R+1),4),'rank_biserial':round(float(rb),2),'ties':int(len(allv)-len(set(allv)))}
# sources table
src=[]
for s,cnt_ in sc.head(13).items():
    d=df[so==s]; t_=sorted(d.TC,reverse=True); h=sum(1 for i,v in enumerate(t_) if v>=i+1)
    src.append([s,int(cnt_),round(100*cnt_/n,1),round(100*cum[s]/tot,1),int(d.TC.sum()),round(d.TC.mean(),1),float(d.TC.median()),h,int(d.PY.min()),int((d.PY>=2024).sum())])
M['sources']=src
# affiliations distinct
aff=collections.defaultdict(set); occ=collections.Counter()
for i,s in df.AU_UN.items():
    if isinstance(s,str):
        parts=[x.strip() for x in s.split(';') if x.strip()]
        for a in set(parts): aff[a].add(i)
names=['CHINA EARTHQUAKE ADMINISTRATION','CHINESE ACADEMY OF SCIENCES','UNIVERSITY OF SCIENCE AND TECHNOLOGY OF CHINA, CAS','INSTITUTE OF GEOPHYSICS, CEA','STANFORD UNIVERSITY','CENTRE NATIONAL DE LA RECHERCHE SCIENTIFIQUE (CNRS)','ISTITUTO NAZIONALE GEOFISICA E VULCANOLOGIA (INGV)','HELMHOLTZ ASSOCIATION','CHINA UNIVERSITY OF GEOSCIENCES','INSTITUTE OF GEOLOGY AND GEOPHYSICS, CAS','UNIVERSIDADE DA BEIRA INTERIOR','UNIVERSITY OF TOKYO']
M['aff']={a:[len(aff[a]),int(df.loc[list(aff[a])].TC.sum()),round(df.loc[list(aff[a])].TC.mean(),1),int(df.loc[list(aff[a])].PY.min())] for a in names}
# removed record contribution to Bibliometrix occurrence counts
r=df0[bad].iloc[0]; M['removed']={'AU_UN':[x.strip() for x in r.AU_UN.split(';')],'C1_countries':sorted(countries(r.C1)),'TC':int(r.TC),'SO':r.SO,'PY':int(r.PY),'corr_country':'SWITZERLAND'}
json.dump(M,open('m197.json','w'),indent=1,default=str)
for k,v in M.items():
    if k not in ('lorenz','lotka'): print(k,':',v)
