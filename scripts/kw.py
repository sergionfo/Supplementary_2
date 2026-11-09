import pandas as pd, re, collections, json
df=pd.read_pickle('sel197.pkl')
syn={}
for line in open('/tmp/supp/biblioshiny_synonyms.txt'):
    p=[x.strip() for x in line.strip().split(',') if x.strip()]
    for x in p[1:]: syn[x]=p[0]
syn.update({'neural network':'neural networks','neural-network':'neural networks','convolutional neural network':'cnn','convolutional neural networks':'cnn','deep learning (dl)':'deep learning','earthquakes':'earthquake','seismic phase picking':'phase picking','transformer':'transformer','transformers':'transformer','transfer-learning':'transfer learning'})
remove=set('phase picking,phase picker,phase detection,earthquake detection,deep learning,artificial intelligence,machine learning,support vector machines,svm,ai,ml,earthquake,neural networks,picking,seismic phase picking'.split(','))
c=collections.Counter(); n=0
for s in df['DE'].dropna():
    n+=1
    ks={syn.get(k.strip().lower(),k.strip().lower()) for k in s.split(';') if k.strip()}
    for k in ks:
        if k not in remove: c[k]+=1
print('docs with DE',n); print(c.most_common(30))
json.dump(c.most_common(60),open('de_freq.json','w'))
# lexical coding of title+abstract+DE
txt=(df['TI'].fillna('')+' '+df['AB'].fillna('')+' '+df['DE'].fillna('')).str.lower()
fam={
 'CNN / U-Net':r'\bcnn|convolution|u-?net\b|unet',
 'RNN / LSTM / GRU':r'\brnn\b|recurrent|lstm|\bgru\b',
 'Transformer / attention':r'transformer|attention|self-attention',
 'Graph / multi-station':r'graph neural|\bgnn\b|graph convolution|multi-station|multistation|neural operator',
 'Capsule network':r'capsule',
 'Generative (GAN / diffusion / VAE)':r'generative adversarial|\bgan\b|diffusion model|variational autoencoder',
 'Classical ML (SVM / RF / boosting)':r'support vector|\bsvm\b|random forest|xgboost|gradient boosting|k-nearest',
 'Transfer learning / fine-tuning':r'transfer learning|transfer-learn|fine-tun',
 'Semi/self-supervised, unsupervised':r'semi-supervised|self-supervised|unsupervised|contrastive',
 'Uncertainty / Bayesian / ensemble':r'uncertaint|bayesian|ensemble',
 'Lightweight / edge / real-time':r'lightweight|light-weight|edge device|embedded|low-cost|mems|real-time|realtime',
 'Physics-informed':r'physics-informed|physics informed|physics-guided',
}
rows=[]
for k,pat in fam.items():
    m=txt.str.contains(pat,regex=True)
    by=df.loc[m,'PY'].value_counts().to_dict()
    rows.append([k,int(m.sum())]+[int(by.get(y,0)) for y in [2020.,2021.,2022.,2023.,2024.,2025.]])
fr=pd.DataFrame(rows,columns=['Family','Total','2020','2021','2022','2023','2024','2025']); print(fr.to_string())
fr.to_json('families.json',orient='records')
ds={'STEAD':r'\bstead\b','INSTANCE':r'\binstance\b(?! segmentation)','DiTing':r'diting','SCEDC / SCSN (S. California)':r'scedc|scsn|southern california','NCEDC (N. California)':r'ncedc|northern california','Japan (Hi-net / JMA)':r'hi-net|\bjma\b|japan','Taiwan':r'taiwan','Ocean-bottom seismometers':r'ocean[- ]bottom|\bobs\b','Volcanic settings':r'volcan','SeisBench':r'seisbench'}
rows=[]
for k,pat in ds.items():
    m=txt.str.contains(pat,regex=True); rows.append([k,int(m.sum())])
print(rows); json.dump(rows,open('datasets.json','w'))
m=txt.str.contains(r'azores|açores|acores|são jorge|sao jorge|são miguel|sao miguel|terceira|faial'); print('azores',df.loc[m,['TI','PY']].to_string())
print(df['DT'].value_counts())
