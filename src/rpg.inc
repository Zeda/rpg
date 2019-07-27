;OS equates
_JForceCmdNoChar= 4027h
_delRes     = 4A20h
_CreateVar  = 4E70h
_CreateAppVar=4E6Ah
_DeleteTempPrograms = 5041h
_CleanAll   = 4A50h
_Delvar     = 4351h
_DelvarArc  = 4FC6h
_ChkFindSym = 42F1h
_CreateGDB  = 4336h
_Arc_Unarc  = 4FD8h
rMov9ToOP1  = 20h
statVars    = 8A3Ah
flags       = 89F0h
appBackUpScreen = 9872h
plotSScreen = 9340h
OP1         = 8478h
ProgObj     = 5
GDBObj      = 8
tVarGDB     = 61h

#define _Erase  0
#define _OR     1
#define _XOR    2
#define Rect(y,x,h,w,m)  call irect \ .db y,x,h,w,m

#define K_DELAY_DEFAULT 13
#define K_DELAY_ACCEL 3
#define TEMP_ALLOC_MAX 3000
#define SAVE_SIZE 350     ;3 bytes "RPG" 2 bytes map ID, 2 bytes coordinates, 10 bytes name, 1 byte 0, 4 bytes ID+direction, 128 bytes flags, 200 bytes items.
#define P_NAME 7
#define RAMCode $8002
maskbuf   = appBackUpScreen
topbuf    = plotSScreen
backup    = $8DA1-74
rpgRAM    = 86E2h       ;1653 bytes
gbuf      = rpgRAM      ;1120 bytes
parse_stack=8B42h       ;end of gbuf, stack gets 190 bytes

player_flags = 22

#define scrap $8C00 ; 343 bytes
spsave    = scrap
sprites   = scrap+2
map_base  = scrap+4
map_UL    = scrap+6
map_UR    = scrap+8
coord     = scrap+10    ;used during intermediate drawing
draw_ptr  = scrap+12    ;used in the tilemap drawing routine
tile_ptr  = scrap+14    ;used in the tilemap drawing routine

psprite           = scrap+16
player_tile_base  = scrap+18
player_sprite_base= scrap+20
p_direction       = scrap+22
temp_prog_base    = scrap+24
incnt             = scrap+26
inloc             = scrap+28
event_code        = scrap+30
k_save            = scrap+32
k_count           = scrap+33
k_delay           = scrap+34
oldtile_mapedit   = scrap+35    ;Only used during map editing
curtile_mapedit   = scrap+36    ;
player_save       = scrap+37
seed0             = scrap+39    ; 4 bytes
seed1             = scrap+43    ; 4 bytes
curbuf            = scrap+47
textcol           = scrap+49
textrow           = scrap+50
textbase          = scrap+52
map_height= scrap+82
map_width = map_height+1
map_y     = map_width+1
map_x     = map_y+1
tile_count= map_x+1
tile_table= tile_count+1

rpgflags  = 33
updateLCD = 0   ;Tells the interrupts to update the LCD
drawmap   = 1   ;Tells the interrupts to redraw the map
animate   = 2   ;Tells the interrupts to animate tiles
noupdate  = 3   ;Overrides the interrupt's LCD update and tilemap redraw

mapedit   = 6
keepmap   = 7
