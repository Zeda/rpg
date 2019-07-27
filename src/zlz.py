#
# THIS IS A MODIFIED VERSION
# it prepends the data with size bytes
#

import sys
import numpy as np
help=sys.argv[0]+""" file1
"""
minsize=4
cc = 0
def size(n,num=True,j=0):
    if num==True:
        b=n&127
        if n>=128:
            b|=128
        n>>=7
    else:
        b=n&63
        if n>=64:
            b|=64
        n>>=6
        b|=j
    s=[b]
    while n>=128:
        s+=[(n&127)|128]
        n>>=7
    if n>0:
        s+=[n]
    if len(s)>3:
        print("Warning: Block size is too large for some Z80 decompressors.")
    return np.array(s,dtype=np.uint8)
def comp(s):
    global cc
    n=len(s)
    if n==0:
        np.tofile(out,s)
        return s
    if n<=minsize:
        s=np.append(np.array([n],dtype=np.uint8),s)
        s.tofile(out)
        return s
    head=minsize
    tail=minsize
    t=np.array([],dtype=np.uint8)
    base=0
    cnt=128
    cc=10
    while tail<=n-minsize:
        head=tail
        srch=0
        match=[0,0,minsize-1]
        while srch<head:
            while s[head]!=s[srch]:
                srch+=1
            if srch<head:
                u=head
                v=srch
                k=0
                while s[u]==s[v] and u<n-1:
                    u+=1
                    v+=1
                    k+=1
                if s[u]==s[v]:
                    u+=1
                    v+=1
                    k+=1
                if k>=match[2]:
                    match=[u,v,k]
            srch+=1
        if match[2]>=minsize:
            u=match[0]
            v=match[1]
            k=match[2]
            m=s[base:tail]
            if len(m)>0:
                t=np.append(t,size(len(m),False))
                t=np.append(t,m)
                cc+=218+21*len(m)
                if len(m)>=64:
                    cc+=111
            cc+=285+21*k
            if k>=64:
                cc+=111
            if tail-v+k>=64:
                cc+=115
            t=np.append(t,np.array(size(k,False,128),dtype=np.uint8))
            t=np.append(t,np.array(size(tail-v+k),dtype=np.uint8))
            tail+=k
            base=tail
            if tail>=cnt:
                cnt+=128
        else:
            tail+=1
    if base<n:
        m=s[base:n]
        t=np.append(t,size(len(m),False))
        t=np.append(t,m)
    return t
def parse(cmd):
    global cc
    cc = 0
    if len(sys.argv)==1:
        print(help)
        return

    if len(sys.argv)<3:
        out=sys.argv[1]+".zcmp"
    else:
        out=sys.argv[2]

    if len(sys.argv)<4:
        lbl = 'data'
    else:
        lbl = sys.argv[3]

    infile=sys.argv[1]
    if infile[-4:-1].lower()==".8x":
        print("I'm lazy, so just assuming this is a TI Variable")
        s=np.fromfile(infile,dtype=np.uint8)[74:-2]
    else:
        s=np.fromfile(infile,dtype=np.uint8)
    n = len(s)
    print("%d bytes in" %(n))
    t = comp(s)
    print("%d bytes out" %(len(t)))
    print("Ratio: %d%%" %(len(t)*100/n))
    print("Decompression Speed for LZD %dcc, about %f times slower than LDIR" %(cc,cc/(21*n-5.0)))
    if out[-4:]==".z80" or out[-4:]==".asm":
        f=open(out,'w')
        f.write(lbl+':\n')
        f.write('.dw '+lbl+'_end-2-'+lbl)
        k=16
        hx='0123456789ABCDEF'
        for i in t:
            if k==16:
                k=0
                f.write('\n.db $')
            else:
                f.write(',$')
            f.write(hx[i>>4]+hx[i&15])
            k+=1
        f.write('\n'+lbl+'_end:')
        f.close()
    else:
        t.tofile(out)
    return t
parse(sys.argv)
