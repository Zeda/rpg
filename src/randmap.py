for i in range(20):
  s=".db "
  for j in range(20):
    s+=str((i&j)%5)+","
  print(s[0:-1])