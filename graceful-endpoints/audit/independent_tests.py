import itertools
import json
from pathlib import Path
from construct import carrier, construct, ray

def validate(seq,n,a,b):
    assert len(seq)==n and seq[0]==a and seq[-1]==b
    assert set(seq)==set(range(n))
    jumps=[abs(y-x) for x,y in zip(seq,seq[1:])]
    assert set(jumps)==set(range(1,n))

def is_adm(n,a,b):
    return a!=b and (b-a-n*(n-1)//2)%2==0 and 2*abs(b-a)<=n and n-1<=2*(a+b)<=3*(n-1)

for path in json.loads(Path(__file__).with_name('seeds.json').read_text()):
    validate(path,len(path),path[0],path[-1])
count=0
for L in range(2,81):
    h=L//2
    for H in ([h-1,h] if L%2 else [h-1]):
        if L%2==0: pairs=[(u,u+h) for u in range(h)]
        elif H==h: pairs=[(u,h-u) for u in range((h+1)//2)]
        else: pairs=[(u,3*h-u) for u in range(h,(3*h+1)//2)]
        for u,v in pairs:
            candidates={(0,L-1),(H,H+1)}
            for i in range(H+1):
                if u==0: candidates.add((i,L-i))
                if v==L-1: candidates.add((i,L-2-i))
                if min(u,L-1-v)<i: candidates.add((i,L-1-i))
            for i,j in candidates:
                if not (0<=i<=H<j<L): continue
                q=carrier(L,H,u,v,(i,j))
                validate(q,L,u,v)
                assert all((p<=H)!=(s<=H) for p,s in zip(q,q[1:]))
                assert any(min(p,s)==i and max(p,s)==j for p,s in zip(q,q[1:]))
                count+=1
print('marked carrier instances:',count,flush=True)
count=0
for n in range(2,51):
    for a,b in itertools.product(range(n),repeat=2):
        if is_adm(n,a,b):
            validate(construct(n,a,b),n,a,b)
            count+=1
print('all ordered endpoint triples through length 50:',count,flush=True)
for k in list(range(2,20))+[37,83]:
    validate(ray(k),28*k+22,9*k+7,13*k+10)
print('direct exceptional-progression checks: 20',flush=True)
