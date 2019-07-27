#include "gfx/gfx.inc"
#include "items.inc"

#define selectevent(y,x,d,c) .db y,x,d \ .dw c-$-1

#define num(n)          .db $0B,n
#define ifflag(n)       .db $10 \ .dw n \ .db $0D
#define ifnflag(n)      .db $10 \ .dw n \ .db $23,$0D
#define warp(m,y,x)     .db $0F,m,y-5,x-6
#define settile(y,x,t)  .db $15,y-5,x-6,t
#define jump(n)         .db $0E \ .dw n-$-1
#define dialog(n)       .db $13 \ .dw n-$-2

#define setflag(n)      .db $11 \ .dw n
#define getflag(n)      .db $10 \ .dw n
#define resflag(n)      .db $12 \ .dw n

#define asprite(r,c,s)      .db $1B \.dw c*64+r,s
#define sprite(y,x,s)       .db $1C,y,x \ .dw s
#define shiftsprite(r,c,d,n)  .db $1D,c,d,n
#define disp()                .db $1E
#define noupd()               .db $1F
#define upd()                 .db $20
#define tilesheet(t)          .db $21 \ .dw t
#define playersheet(t)        .db $22 \ .dw t
#define pause(t)              .db $27,t
#define select(p)             .db $28 \ .dw p
#define inputname(n,s)        .db $29 \ .dw n \ .db s
#define additem(i,n)          .db $2A,i,n

pname         = 7
