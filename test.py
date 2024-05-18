import matplotlib.pyplot as plt

# r=100

# n=6000
# t=1
# l1=[]
# for i in range(r):
#     l1.append(n*t/100)
#     n-=n*t/100
#     t=t*1.01

# l=[]
# n=6000
# t=1
# for i in range(r):
#     l.append(n*t/100)
#     n-=n*t/100
#     t=t

# n=6000
# t=1
# l2=[]
# for i in range(r):
#     l2.append(n*t/100)
#     n-=n*t/100
#     t=t*0.99

# plt.plot(l,label='t=1')
# plt.plot(l1,label='t*=1.01')
# plt.plot(l2,label='t*=1.02')
# plt.legend(loc='upper right')
# plt.show()
m=6000
t=1
r=200
x=[]
for i in range(r):
    x.append(i+1)

for k in range(20):
    m=6000
    t=1
    re=[]
    ak=(k+990)/1000
    
    for i in range(r):
        # re.append(m*t/100)
        m-=m*t/100
        t=t*ak
        re.append(m)
    print(re)
    if ak==1:
        plt.plot(x,re,label='k='+str(ak),color="b")
    else:
        plt.plot(x,re,label='k='+str(ak))
plt.legend(loc='upper right')
plt.show()

