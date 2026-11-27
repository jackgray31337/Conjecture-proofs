"""Construct and check the path for r a b. Uses the witnesses of coverage.py."""
import sys
from functools import lru_cache
from coverage import read_seeds, regions, witness

SEEDS = read_seeds()


def check_path(path, n, a, b):
    if (len(path) != n or (path[0],path[-1]) != (a,b)
        or sorted(path) != list(range(n))
        or sorted(abs(x-y) for x,y in zip(path,path[1:])) != list(range(1,n))):
        raise ValueError(f"Invalid output for {(n,a,b)}")
    return tuple(path)


def complement(path):
    return tuple(len(path)-1-x for x in path)


def walecki(n):
    return tuple(i//2 if i%2==0 else n-1-i//2 for i in range(n))


def prefix(block, inner):
    c = len(block)//2
    return tuple(x if x<c else x+len(inner) for x in block) + tuple(x+c for x in inner)


@lru_cache(None)
def even(h,u):
    if 2*u > h-1:
        return complement(even(h,h-1-u)[::-1])
    if u==0:
        return walecki(2*h)
    if 2*u==h-1:
        w=walecki(2*h)
        return (w[h:]+w[:h])[::-1]
    c=h//2
    return prefix(even(c,u),even(h-c,u))


def odd(h,u):
    if 2*u>h:
        return odd(h,h-u)[::-1]
    if 2*u==h:
        raise ValueError("The odd carrier would repeat its endpoint.")
    if u==0:
        return walecki(2*h+1)
    return prefix(even(h-u,u),walecki(2*u+1)[::-1])


def carrier(L,H,U,V,edge=None):
    h=L//2
    if L%2 and H<h:
        # Reflection also reverses the ordering of the target endpoint labels.
        mirror=None if edge is None else (L-1-edge[1],L-1-edge[0])
        return complement(carrier(L,h,L-1-V,L-1-U,mirror)[::-1])
    if not L%2 and 2*U>h-1:
        mirror=None if edge is None else (L-1-edge[1],L-1-edge[0])
        return complement(carrier(L,H,L-1-V,L-1-U,mirror)[::-1])
    base = odd(h,U) if L%2 else even(h,U)
    if edge is None or contains(base,edge):
        return base
    i,j=edge
    if i+j!=L-1 or i<=U:
        raise ValueError("No certified marked-edge construction")
    for c in (i,i+1):
        if c<=U or c>=h:
            continue
        if L%2:
            if h-c<U or h-c==2*U:
                continue
            inner=odd(h-c,U)
        else:
            if h-c<=U:
                continue
            inner=even(h-c,U)
        candidate=prefix(even(c,U),inner)
        if contains(candidate,edge):
            return candidate
    # Large i belongs to the central reversed/complemented Walecki segment.
    if not L%2 and h>2*U+1:
        c=h-U-1
        candidate=prefix(even(c,U),complement(walecki(2*(U+1))[::-1]))
        if contains(candidate,edge):
            return candidate
    raise ValueError(f"Missing claimed carrier {(L,H,U,V,edge)}")


def contains(path,edge):
    return any(tuple(sorted((x,y)))==edge for x,y in zip(path,path[1:]))


def splice(path,edge,replace):
    """Insert replace (listed from high to low) along an unordered edge."""
    i,j=edge
    for idx,(a,b) in enumerate(zip(path,path[1:])):
        if {a,b}=={i,j}:
            return path[:idx+1]+(replace if a==j else replace[::-1])+path[idx+1:]
    raise ValueError("Missing marked edge")


def insertion(path,j):
    m=len(path)
    x,y=next(sorted((i,k)) for i,k in zip(path,path[1:]) if abs(i-k)==j)
    if y>=2*j:
        if m-1-x>=2*j:
            raise ValueError("Neither orientation admits insertion.")
        return complement(insertion(complement(path),j))
    shifted=tuple(v+2*j for v in path)
    block=tuple(v if v<2*j else v+m for v in even(2*j,y))
    return splice(shifted,(x+2*j,y+2*j),block[::-1])


def ray(k):
    u,j=k+1,4*k+3
    c=j+2
    q=u+2
    inner=construct(4*k,k+1,k-1)
    six=(1,5,0,3,2,4)
    protected=complement(prefix(even(q-3,1),six)[::-1])
    block=prefix(even(c-q,u),protected)
    return insertion(prefix(block,inner),j)


def edge_move(move,kind,params):
    h,m,z,U,V,x,y=(params[w] for w in ("h","m","z","U","V","x","y"))
    L=2*h+(kind!=1)
    H=h if kind==0 else h-1
    off=int(move=="D")
    r=L+m+2*z-off
    i,j=(0,L-1) if off else (params["i"],params["j"])
    base=carrier(L,H,U,V,None if off else (i,j))
    old=tuple(t+z-off+(m if t>H else 0) for t in base)
    core=tuple(t+z-off+H+1 for t in construct(m,x,y))
    if off:
        outer=tuple(t for k in range(z) for t in (r-1-k,k))
        # Its last vertex is already the image of base label zero.
        bridge=core+outer[:-1]
    else:
        e=H+1+y
        if not 0<=e<z:
            e+=j-i-L
        outer=tuple(t if t<z else t+L+m for t in even(z,e)[::-1])
        bridge=core+outer
    return splice(old,(i+z-off,j+z-off+m),bridge)


@lru_cache(None)
def construct(r,a,b):
    if not (0<=a<r and 0<=b<r and a!=b and (a-b-r//2)%2==0
            and 2*abs(a-b)<=r and r-1<=2*(a+b)<=3*(r-1)):
        raise ValueError("Inadmissible endpoints")
    if a>b:
        return construct(r,b,a)[::-1]
    if a+b>=r:
        return complement(construct(r,r-1-b,r-1-a)[::-1])
    if (r,a,b) in SEEDS:
        return SEEDS[r,a,b]
    for tag,variables,formula in regions():
        params=witness(formula,variables,r,a,b)
        if params is None:
            continue
        move,index=tag[:2]
        u,v=[(a,b),(r-1-b,r-1-a),(b,a),(r-1-a,r-1-b)][index]
        if move=="A":
            c=params["c"]
            path=prefix(even(c,u),construct(r-2*c,u,v-c))
        elif move=="B":
            j=params["j"]
            path=insertion(construct(r-4*j,u-2*j,v-2*j),j)
        elif move=="C":
            c=params["c"]
            m=r-2*c-1
            block=tuple(t if t<=c else t+m for t in odd(c,u))
            inner=complement(construct(m,u,r-1-c-v))
            path=block+tuple(t+c+1 for t in inner)
        elif move=="ray":
            path=ray(params["k"])
        else:
            path=edge_move(move,tag[2],params)
        if index in (1,3):
            path=complement(path)
        if index in (1,2):
            path=path[::-1]
        return check_path(path,r,a,b)
    raise RuntimeError("Uncovered instance")


if __name__=="__main__":
    r,a,b=map(int,sys.argv[1:])
    print(*check_path(construct(r,a,b),r,a,b))
