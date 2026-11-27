"""Independent forward-image audit of proposed constructions, in zero-based labels."""
import ctypes as ct
from ctypes.util import find_library
import json
from pathlib import Path
s=ct.CDLL(find_library('isl'))
P=ct.c_void_p
def bind(n,ret,*sig):
    f=getattr(s,'isl_'+n)
    f.argtypes=list(sig); f.restype=ret
    return f
ctx=bind('ctx_alloc',P)()
def ptr(p):
    if not p: raise RuntimeError('isl error')
    return p
read=bind('set_read_from_str',P,P,ct.c_char_p)
readmap=bind('map_read_from_str',P,P,ct.c_char_p)
rng=bind('map_range',P,P)
apply=bind('set_apply',P,P,P)
minus=bind('set_subtract',P,P,P)
simp=bind('set_coalesce',P,P)
copy=bind('set_copy',P,P)
drop=bind('set_free',P,P)
equal=bind('set_is_equal',ct.c_int,P,P)
def st(x): return ptr(read(ctx,x.encode()))
def mp(x): return ptr(readmap(ctx,x.encode()))
def admiss(n,x,y):
    # 4 residue classes for parity of the triangular number; no division.
    parity=f'((({n}%4=0 or {n}%4=1) and ({x}+{y})%2=0) or (({n}%4=2 or {n}%4=3) and ({x}+{y})%2=1))'
    return f'{n}>=2 and 0<={x}<{n} and 0<={y}<{n} and ({x}<{y} or {x}>{y}) and 2*({x}-{y})<={n} and 2*({y}-{x})<={n} and 2*({x}+{y})>={n}-1 and 2*(2*{n}-2-{x}-{y})>={n}-1 and '+parity

R=st('{[n,p,q]: p<q and p+q<=n-1 and '+admiss('n','p','q')+'}')
syms=[mp('{[n,p,q]->[n,q,p]}'),mp('{[n,p,q]->[n,n-1-q,n-1-p]}'),mp('{[n,p,q]->[n,n-1-p,n-1-q]}')]
cm=bind('map_copy',P,P)
def remove_image(im,variants=(0,1,2,3)):
    global R
    for ix in variants:
        obj=copy(im) if ix==0 else ptr(apply(copy(im),cm(syms[ix-1])))
        R=ptr(simp(ptr(minus(R,obj))))
    drop(im)
def image(variables,output,conditions,variants):
    rel=mp('{['+variables+']->['+output+']: '+conditions+'}')
    remove_image(ptr(rng(rel)),variants)
inn=admiss('m','x','y')
# Parameterise the two prefixes by the inner path in its actual orientation.
image('m,x,y,c','m+2c,x,y+c',inn+' and 0<=x<c',(0,1,2,3))
image('m,x,y,j','m+4j,x+2j,y+2j',inn+' and 1<=j<m and m<=3j',(0,))
image('m,x,y,c,u','m+2c+1,u,y+c+1',inn+' and x=m-1-u and 0<=u<=c and u!=c-u',(0,1,2,3))
# Encode the new jumps as equalities before eliminating witness variables.
for mode in ('D','E'):
 for kind in range(3):
    spec=[
      ('L=2h+1 and H=h and U+V=h and V<=H',False,False),
      ('L=2h and H=h-1 and V-U=h and U<=H and V>H',False,True),
      ('L=2h+1 and H=h-1 and U+V=3h and U>H',True,True)
    ][kind]
    base=inn+' and '+spec[0]+' and h>=1 and z>=1 and 0<=U<V<L'
    off='z-1' if mode=='D' else 'z'
    u='U+'+off+('+m' if spec[1] else '')
    v='V+'+off+('+m' if spec[2] else '')
    vars='h,L,H,U,V,m,x,y,z'
    if mode=='D':
        # Image of top carrier label to first inner label; last inner label to top of outer block.
        constraint=' and L-1+z-1+m-(z+H+x)=m and (L+m+2z-2)-(z+H+y)=m+L-1'
        image(vars,'L+m+2z-1,'+u+','+v,base+constraint,(0,2))
    else:
        # First join is m. Remaining two joins must realise m+d and m+L in either order.
        constraints=' and 0<=i<=H<j<L and 0<=e<z and j+z+m-(z+H+1+x)=m'
        jump2='(L+m+z+e-(z+H+1+y))'
        jump3='(z+i-e)'
        constraints+=f' and (({jump2}=m+L and {jump3}=m+j-i) or ({jump3}=m+L and {jump2}=m+j-i))'
        conditions=['i=0 and j=L-1','i=H and j=H+1','((U=0 and i+j=L) or (V=L-1 and i+j=L-2))','i+j=L-1 and (i>U or L-1-i<V)']
        for cond in conditions:
            image(vars+',i,j,e','L+m+2z,'+u+','+v,base+constraints+' and '+cond,(0,2))
image('k','28k+22,9k+7,13k+10','k>=2',(0,))
paths=json.loads(Path(__file__).with_name('seeds.json').read_text())
seeds=st('{'+ ';'.join(f'[{len(p)},{p[0]},{p[-1]}]' for p in paths)+'}')
status=equal(R,seeds)
print('remaining forward-image complement equals enumerated seeds:',status, len(paths),flush=True)
assert status==1
