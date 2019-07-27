hx="0123456789ABCDEF"
def remap(fi,fo):
  f=open(fi,'r')
  s=f.read()
  f.close()
  o='sprites:'
  f=False
  m=[]
  for i in s.split("\r\n")[0:-1]:
    if i!="":
      if i[-1]!=":":
        if f:
          #need to put the output into the map
          m+=[i[4:].split(",")]
        else:
          #reformat the sprites
          s='\n.db '
          for j in i[5:].split(",%"):
            s+="$"+hx[int(j[:4],2)]+hx[int(j[4:],2)]+","
          o+=s[:-1]
      else:
        if i=="map:":
          f=True
  o+='\nmap:\n.db '+str(len(m[0]))+","+str(len(m))+"\n.db -3,-3\n .db "
  mp=''
  n=0
  for i in range(len(m[0])):
    mp+="\n.db "
    for j in range(len(m)):
      x=m[j][i]
      mp+=x+","
      if int(x)>n:
        n=int(x)
    mp=mp[0:-1]
  o+=str(n)
  for i in range(n):
    o+="\n.dw tile"+str(i)
  f=open(fo,'w')
  f.write(o)
  f.write(mp)
  for i in range(n):
    f.write("\ntile"+str(i)+":  .db "+str(i)+",0 \ .dw tile"+str(i))
  f.close()
remap("spritemap.z80","map.z80")