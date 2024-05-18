import matplotlib.pyplot as plt

x=[]
mwd=[]
pwd=[]
for i in range(1,51):
    x.append(i)
    mwd.append(50+i)
    pwd.append(50-i)

plt.bar(x,mwd,width=-1,label='main wallet',edgecolor='grey',zorder=5,align='edge')
plt.bar(x,pwd,width=-1,bottom=mwd,label='pledge wallet',edgecolor='grey',zorder=5,align='edge')
plt.tick_params(axis='x',length=0)
plt.grid(axis='y',alpha=0.5,ls='--')
# plt.ylim(0,1600)
plt.xlim(0,50)
plt.legend(loc='upper left')
# plt.tight_layout()
# plt.savefig('bar1.png', dpi=600)
plt.show()