import os,sys,pygame
from math import sin,cos
from random import random
import zlz

pygame.init()
pygame.mixer.quit()     #This eats up a core of resources, so let's close it!
black=(0,0,0)
white=(255,255,255)
srcout = "../src/maps/"

def window(width=800,height=600):
    return pygame.display.set_mode((width,height))

def pixel(screen,x,y,c,w=16,h=16):
  for i in range(w):
    for j in range(h):
      screen.set_at((x+i,y+j),c)

def tilepix(screen,pos,tile,color):
  x = ((pos[0] - 800 - 4 - 512 - 4)&0xFFF0)
  y = pos[1]&0xFFF0
  pixel(screen,x+800+4+512+4,y,color)
  cy = tile >> 4
  cx = tile & 15
  cy <<= 5
  cx <<= 5
  pixel(screen,(x>>2)+cx+800+4,cy+(y>>2),color,4,4)

def img2hex(scr):
  s = '.db $'
  for y in range(8):
    acc = 0
    for x in range(8):
      acc += acc
      if scr.get_at((x,y)) != white:
        acc += 1
    acc = hex(acc)[2:].upper()
    s += "0"*(2-len(acc)) + acc + ',$'
  return s[0:-2]

def rand():
#  return random()
  return random()*2-1

def toggletile(screen,x,y):
  for i in range(16):
    for j in range(16):
      c = screen.get_at((x+i,y+j))
      screen.set_at((x+i,y+j),(c[0]^64,c[1]^64,c[2]^64))

def drawmap(screen,anim,mapdata,tile):
  y = 0
  for i in mapdata:
    x = 0
    for j in i:
      screen.blit(pygame.transform.scale(tile[anim[j&255][0]],(16,16)),pygame.Rect(x,y,16,16))
      if j>=256:
        toggletile(screen,x,y)
      x += 16
    y += 16
def savez80(s):
  return
def animate(screen,anim,mapdata,tile):
  rerender = False
  for i in range(256):
    if anim[i][1] != 0:
      anim[i][1] -= 1
      if anim[i][1] == 0:
        rerender = True
        t = anim[i][2]
        anim[i][0] = anim[t][3]
        anim[i][1] = anim[t][4]
        anim[i][2] = anim[t][5]
  if rerender:
    drawmap(screen,anim,mapdata,tile)
    pygame.display.flip()
  return anim
anim = []
for i in range(256):
  anim += [[i,0,i,i,0,i]]

anim[14] = [14,32,15,14,32,15]
anim[15] = [15,32,14,15,32,14]

anim[16] = [16,32,17,16,32,17]
anim[17] = [17,32,16,17,32,16]

anim[58] = [58,16,59,58,16,59]
anim[59] = [59,16,58,59,16,58]

anim[69] = [69,240,71,69,240,71]
anim[71] = [71,240,69,71,240,69]

anim[70] = [70,32,72,70,32,72]
anim[72] = [72,32,70,72,32,70]

for i in range(8):
  anim[23+i] = [23+i,32,31+i,23+i,32,31+i]
  anim[31+i] = [31+i,32,23+i,31+i,32,23+i]


# Initialize the window
screen=window(800+4+512+4+128+1,800)
screen.fill(white)

# Define rectangles
tiles = pygame.Rect(800+4,0,512,512)
tilemap = pygame.Rect(0,0,800,800)
edit = pygame.Rect(800+4+512+4,0,128,800)
templates = pygame.Rect(800+4,512,512,288)

# Load the tiles
timg = pygame.image.load("tiles.png")
tile = []
x = 0
y = 0
for k in range(256):
  img = pygame.Surface((8,8)).convert()
  img.blit(timg,(0,0),pygame.Rect(x,y,x+8,y+8))
  tile += [img]
  x += 8
  if x == 128:
      x = 0
      y += 8

# Load the desired map
mapname = "map0.txt"
try:
  f = open(mapname,'r')
  s = f.read().replace('\r','\n').replace('\n\n','\n').split('\n')
  f.close()
except:
  s = ['1','1','0']

mapw = int(s[0])
maph = int(s[1])
mapdata = []
for i in range(50):
  mapdata += [[0]*50]

for i in range(maph):
  r = s[i+2].split(',')
  for j in range(len(r)):
    mapdata[i][j] = int(r[j])

drawmap(screen,anim,mapdata,tile)

t = pygame.transform.scale(timg,(512,512))
screen.blit(t,tiles)
for y in range(800):
  for k in range(2):
    screen.set_at((801+k,y),black)
    screen.set_at((801+4+512+k,y),black)

for x in range(128):
    screen.set_at((800+4+512+4+x,129),black)
    screen.set_at((800+4+512+4+x,130),black)

# Display it in the tile editor menu
screen.blit(pygame.transform.scale(tile[0],(128,128)),edit)

# Load tile templates
#f = open('templates.txt','r+')
#s = f.read().replace('\r','\n').replace('\n\n','\n').split('\n')
#f.close()


pygame.display.flip()
draw = False
tileselected = False
curtile = 0
tilesedited = False
last_x = 0
last_y = 0
color  = black
kup = True
pygame.time.set_timer(pygame.USEREVENT+1, 8)
while 1:
    pygame.time.wait(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          # screenshot
          pygame.image.save(screen,"tilemap.png")

          # Save the tilesheet
          if tilesedited:
            x = 0
            y = 0
            for i in range(256):
              timg.blit(tile[i],pygame.Rect(x,y,x+8,y+8))
              x += 8
              if x == 128:
                x = 0
                y += 8
            pygame.image.save(timg,"tiles.png")

          # Save the tilemap
          # Get the dimensions of the map
          x = 0
          y = 0
          a = 0
          for i in mapdata:
            c = 0
            k = 0
            for j in i:
              if j != 0:
                c = k
              k += 1
            if c != 0:
              y = a
            a += 1
            if c>x:
              x = c
          x += 1
          y += 1
          s = str(x)+'\n'+str(y)
          for i in mapdata[0:y]:
            t = '\n'
            for j in i[0:x]:
              t += str(j)+','
            s += t[0:-1]
          f = open(mapname,'w')
          f.write(s)
          f.close()
          print("saved "+mapname)
          sys.exit()
        elif event.type == pygame.USEREVENT+1:
          anim = animate(screen,anim,mapdata,tile)
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            #Check if we are hovering over the map editor
            #tile editor, or tile select
            if event.pos[0]<800:
              # map editor
              #need to map pos to map coords
              x = event.pos[0]>>4
              y = event.pos[1]>>4

              #edit map data
              mapdata[y][x] = curtile

              #draw tile
              screen.blit(pygame.transform.scale(tile[curtile],(16,16)),pygame.Rect(x<<4,y<<4,16,16))

              pygame.display.flip()

            elif event.pos[0]<800+4+512:
              # tile selector
              curtile = ((event.pos[0]-800-4)>>5) + (((event.pos[1])>>5)<<4)

              # Now we need to display it in the tile editor menu
              screen.blit(pygame.transform.scale(tile[curtile],(128,128)),edit)

              pygame.display.flip()

            else:
              # tile editor
              last_x = event.pos[0]
              last_y = event.pos[1]
              if y<128:
                if screen.get_at(event.pos)[0] == 0:
                  color = white
                else:
                  color = black

                tilepix(screen,event.pos,curtile,color)

                # Need to tilepix the pixel
                i = (curtile + (last_y>>7))&255
                y = last_y&0x70
                x = (last_x - 800-4-512-4)&0x70
                y >>= 4
                x >>= 4
                tile[i].set_at((x,y),color)

                #Need to redraw the map
                drawmap(screen,anim,mapdata,tile)

                pygame.display.flip()
                tilesedited = True
            draw = True
          if event.button == 3:
            # Toggle event tile
            if event.pos[0]<800:
              # map editor
              #need to map pos to map coords
              x = event.pos[0]>>4
              y = event.pos[1]>>4

              #edit map data
              mapdata[y][x] ^= 256

              #draw tile
              toggletile(screen,x<<4,y<<4)

              pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            draw = False
        elif event.type == pygame.MOUSEMOTION and draw:
            if event.pos[0]<800:
              # map editor
              #need to map pos to map coords
              x = event.pos[0]>>4
              y = event.pos[1]>>4

              #edit map data
              mapdata[y][x] = curtile

              #draw tile
              screen.blit(pygame.transform.scale(tile[curtile],(16,16)),pygame.Rect(x<<4,y<<4,16,16))

              pygame.display.flip()
            elif event.pos[0]<800+4+512:
              pass
            else:
              if abs(event.pos[0] - last_x) >= 16 or abs(event.pos[1] - last_y) >= 16:
                last_x = event.pos[0]
                last_y = event.pos[1]
                if last_y <128:
                  tilepix(screen,event.pos,curtile,color)

                  # Need to tilepix the pixel
                  i = (curtile + (last_y>>7))&255
                  y = last_y&0x70
                  x = (last_x - 800-4-512-4)&0x70
                  y >>= 4
                  x >>= 4
                  tile[i].set_at((x,y),color)

                  #Need to redraw the map
                  drawmap(screen,anim,mapdata,tile)

                  pygame.display.flip()
                  tilesedited = True
        elif event.type == pygame.KEYDOWN and kup:
          kup = False
          if event.unicode == u's':
            # screenshot
            pygame.image.save(screen,"tilemap.png")

            # Save the tilesheet
            if tilesedited:
              x = 0
              y = 0
              for i in range(256):
                timg.blit(tile[i],pygame.Rect(x,y,x+8,y+8))
                x += 8
                if x == 128:
                  x = 0
                  y += 8
              pygame.image.save(timg,"tiles.png")

            # Save the tilemap
            # Get the dimensions of the map
            x = 0
            y = 0
            a = 0
            for i in mapdata:
              c = 0
              k = 0
              for j in i:
                if j != 0:
                  c = k
                k += 1
              if c != 0:
                y = a
              a += 1
              if c>x:
                x = c
            s = str(x+1)+'\n'+str(y+1)
            for i in mapdata[0:y+1]:
              t = '\n'
              for j in i[0:x+1]:
                t += str(j)+','
              s += t[0:-1]
            f = open(mapname,'w')
            f.write(s)
            f.close()
            print("saved "+mapname)
          elif event.unicode == u'l':
            mapname = raw_input("Map : ")
            try:
              f = open(mapname,'r')
              s = f.read().replace('\r','\n').replace('\n\n','\n').split('\n')
              f.close()
            except:
              s = ['1','1','0']
            mapw = int(s[0])
            maph = int(s[1])
            mapdata = []
            for i in range(50):
              mapdata += [[0]*50]

            for i in range(maph):
              r = s[i+2].split(',')
              for j in range(len(r)):
                mapdata[i][j] = int(r[j])

            drawmap(screen,anim,mapdata,tile)
            pygame.display.flip()
          elif event.unicode == u'z':
            savez80(mapdata)
            # screenshot
            pygame.image.save(screen,"tilemap.png")

            # Save the tilesheet
            if tilesedited:
              try:
                f = open(srcout+'tiles.z80','r')
                s = f.read()
                f.close()
              except:
                s = ''
              while '\n\n' in s:
                s = s.replace('\n\n','\n')
              s = s.split('\n')
              s += ['']*(256-len(s))
              z80 = ''
              q = ''
              x = 0
              y = 0
              for i in range(256):
                timg.blit(tile[i],pygame.Rect(x,y,x+8,y+8))
                t = img2hex(tile[i])
                q += t+s[i][35:]+'\n'
                if t != '.db $00,$00,$00,$00,$00,$00,$00,$00':
                  z80 += q
                  q = ''
                x += 8
                if x == 128:
                  x = 0
                  y += 8
              pygame.image.save(timg,"tiles.png")
              f = open(srcout+'tiles.z80','w')
              f.write(z80)
              f.close()

            # Save the tilemap
            # Get the dimensions of the map
            x = 0
            y = 0
            a = 0
            for i in mapdata:
              c = 0
              k = 0
              for j in i:
                if j != 0:
                  c = k
                k += 1
              if c != 0:
                y = a
              a += 1
              if c>x:
                x = c
            x += 1
            y += 1
            s = str(x)+'\n'+str(y)
            used = []
            for i in mapdata[0:y]:
              t = '\n'
              for j in i[0:x]:
                if j&255 not in used:
                  used += [j&255]
                t += str(j)+','
              s += t[0:-1]
            f = open(mapname,'w')
            f.write(s)
            f.close()
            used = sorted(used)
            trans = True

            # Now generate the z80 code
            nm = []
            for i in range(x):
              nm += [[0]*y]

            if trans:
              for i in range(y):
                for j in range(x):
                  nm[j][i] = mapdata[i][j]
            z80 = '#include "parse.inc"\n.db ' +str(y) + ',' + str(x) + \
                  '\n.db 0,0' + \
                  '\n.db ' + str(len(used))
            for i in used:
              z80 += '\n.dw '+str(i)

            walking = [0,9,14,15,16,17,39,50,54,73]
            event = [9]

            event_tiles = []
            y = 0
            for i in nm:
              z80 += '\n.db '
              x = 0
              for j in i:
                a = used.index(j&255)
                if j&255 not in walking:
                    a += 128
                if j&255 in event or j>=256:
                    a += 64
                    event_tiles+=[[y,x]]
                x += 1
                t = hex(a).upper()[2:]
                z80 += '$'+'0'*(2-len(t))+t+','
              y += 1
              z80 = z80[0:-1]

            if event_tiles != []:
              z80 += '\n;Event tiles:'
              for i in event_tiles:
                if trans:
                  z80 += '\n;  ('+str(i[0])+','+str(i[1])+')'
                else:
                  z80 += '\n;  ('+str(i[1])+','+str(i[0])+')'
            mn = mapname.split('/')
            s = ''
            for i in mn[0:-1]:
              s += i+'/'
            mn = mn[-1].split('.')
            s += mn[0]
            for i in mn[1:-1]:
              s += i + '.'
            try:
              f = open(srcout+s+'.code','r')
              #code = f.read().replace('\r\n','\n').replace('\n\r','\n').replace('\r','\n')
              code = '#include "maps/'+s+'.code"'
              f.close()
            except:
              code = ".dw onload-$-1\n.dw onselect-$-1\n.dw onclose-$-1\nonload:\nonselect:\nonclose:\n  .db 0"

            if code.startswith("--src--\n"):
              code = rpgscript2bin(code[8:])
            z80 += '\n' + code
            t=s+'.z80'

            f = open(srcout+t,'w')
            f.write(z80)
            f.close()

            os.system("spasm "+srcout+t+" "+srcout+s+'.bin -I ../src')
            zlz.parse(['zlz.py',srcout+s+'.bin',srcout+s+'_comp.z80',s.split('\\')[-1]])
            os.system("rm "+srcout+s+'.bin')

            print("saved "+s)
          elif event.key == pygame.K_UP:
            curtile -= 16
            curtile &= 255
            screen.blit(pygame.transform.scale(tile[curtile],(128,128)),edit)
            pygame.display.flip()
          elif event.key == pygame.K_DOWN:
            curtile += 16
            curtile &= 255
            screen.blit(pygame.transform.scale(tile[curtile],(128,128)),edit)
            pygame.display.flip()
          elif event.key == pygame.K_LEFT:
            curtile -= 1
            curtile &= 255
            screen.blit(pygame.transform.scale(tile[curtile],(128,128)),edit)
            pygame.display.flip()
          elif event.key == pygame.K_RIGHT:
            curtile += 1
            curtile &= 255
            screen.blit(pygame.transform.scale(tile[curtile],(128,128)),edit)
            pygame.display.flip()

        elif event.type == pygame.KEYUP:
          kup = True
