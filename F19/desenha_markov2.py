# Redesenha o diagrama de estados do Exercicio 2 (markov2.png nao estava disponivel)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
pos = {0:(0,0), 1:(0,3.6), 2:(5,3.6), 3:(5,0), 4:(2.5,1.8)}
nomes = {0:'0\ndesligado',1:'1\naquecimento',2:'2\noperação',3:'3\nesfriamento',4:'4\nmanutenção'}
med = {0:'40 min',1:'20 min',2:'60 min',3:'10 min',4:'30 min'}
fig, ax = plt.subplots(figsize=(8,6.5))
for s,(x,y) in pos.items():
    ax.add_patch(Circle((x,y),0.75,fc='#e8f0fb',ec='#1f4e79',lw=2))
    ax.text(x,y+0.08,nomes[s],ha='center',va='center',fontsize=10)
    ax.text(x,y-0.45,med[s],ha='center',va='center',fontsize=8,color='#555')
arestas=[(0,1,'1',0),(1,2,'0,92',0),(1,4,'0,08',0),(2,3,'0,88',0),(2,4,'0,12',0),(3,0,'0,96',0),(3,4,'0,04',0),(4,0,'1',0)]
for a,b,p,rad in arestas:
    ar=FancyArrowPatch(pos[a],pos[b],arrowstyle='-|>',mutation_scale=18,lw=1.5,color='#333',
                       shrinkA=30,shrinkB=30,connectionstyle=f'arc3,rad={rad}')
    ax.add_patch(ar)
    (x1,y1),(x2,y2)=pos[a],pos[b]
    mx,my=(x1+x2)/2,(y1+y2)/2
    ax.text(mx,my+0.15,p,ha='center',fontsize=10,color='#b00',bbox=dict(fc='white',ec='none',pad=1))
ax.set_xlim(-1,6); ax.set_ylim(-1,4.6); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('CMTC do dispositivo - probabilidades de transição e tempos médios')
fig.savefig('markov2.png',dpi=110,bbox_inches='tight')
