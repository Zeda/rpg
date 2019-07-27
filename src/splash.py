from PIL import Image
import numpy as np
from zlz import comp

im = Image.open("gfx/splash.png")
im = im.resize((96,64))
im = im.convert('1')
im.save("gfx/splashmono.png")
im = im.getdata()
n = np.zeros(768,dtype=np.uint8)
k = 0
i = 0
while k<96:
  while k<6144:
    acc = 0
    for l in range(8):
      acc += acc
      if im[k+l] == 0:
        acc += 1
    n[i] = acc
    i += 1
    k += 96
  k -= (6144-8)

t = comp(n)
print("New size is %d bytes, for a savings of %d bytes (%.2f%%)" % (len(t),768-len(t),100-len(t)/7.68))
f=open('gfx/splash_comp.z80','w')
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
f.close()
