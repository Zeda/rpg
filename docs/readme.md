# Tilemap Engine

Hi!

This is a poorly documented tilemap engine intended for use in RPGs, on the
monochrome TI-83+/84+ series of calculators. It features an interrupt-based
interface, smoothscrolling, animated tiles, events, and dialogue boxes.

## Graphics interface

To achieve a reasonable speed at 6MHz, I had to shuffle non-user RAM to make
room for a slightly larger 80x112 graphics buffer for the tilemap. As well, to
make things easier, there are two mask buffers that are rendered on top of
the tilemap buffer. These allow for the presence of overworld sprites (like the
player sprite), and superimposed menus/dialog boxes. In all cases, graphics are
stored vertically aligned as opposed to horizontally aligned (the OS uses
horizontally aligned buffers). This improves most drawing and rendering speeds,
but is awkward to work with.

In general, you should not have to mess with the tilemap buffer. However, to
render an image on top, know that the `maskbuf` gets ANDed on top of the map
buffer, and the `topbuf` gets ORed on top of that data.


### Map Data Format
Maps are formatted as follows:
```
#include "parse.inc"
.db width,height
.db initial_x,initial_y        ;will probably be removed in the future

;tile table:
.db number_of_unique_tiles
.dw first_tile#
.dw second_tile#
.dw ...
.db <<map first column>>
.db <<map second column column>>
...

.dw onload-$-1
.dw onselect-$-1
.dw onclose-$-1
<<eventtile script that gets executed when the player walk on an event tile.>>

onload:
  <<script to be executed on loading the map>>
onclose:
  <<script to be executed on closing the map>>
onselect:
  .db  number_of_select_events
  selectevent(y,x,direction,code_ptr)   ;first event
  selectevent(y,x,direction,code_ptr)   ;second event
  ...

```
For information on scripting, see the [scripting language](#scripting) section.

The data for the tilemap is actually flipped. So the first row of `.db` statements corresponds to the first `column` of the tilemap. Each element is an index into the tile table for that particular map. Further, the top bit is set to 1 if the tile cannot be walked on, 0 if it can. As well, bit 6 is set if walking on the tile triggers an event (executing the eventtile script). This limits each map to 64 unique tiles. However, those tiles can be selected from 65536 possible tiles (but please don't do *that* many).

### Tile Data Format
Tile data needs a sprite, an animation timer, and a pointer to the next tile for
it's next animation frame.
The actual format is:

```
.db sprite_index   ;the index into the spritesheet
.db timer          ;I find a value of 32 to be good
.dw next_tile      ;This is a pointer, not an index
```

### Spritesheet Format
The spritesheet is just an array of raw sprite data in the usual format for
these calcs.

### Rendering
Rendering is performed during interrupts, as well as the tile animation "clock."
If any tile's animation counter reaches 0, the map will be automatically
re-rendered. If the tilemap is re-rendered (either manually or automatically),
then the updateLCD flag will be set to update the LCD.

To update the LCD on the next interrupt:
```
set updateLCD,(iy+rpgflags)
```
This flag automatically resets once the LCD is updated.

To force the map to be redrawn:
```
set drawmap,(iy+rpgflags)
```
This flag automatically resets once the map is redrawn.

To disable tile animation:
```
res animate,(iy+rpgflags)
```

To enable tile animation:
```
set animate,(iy+rpgflags)
```

To override LCD updates and tilemap re-rendering:
```
set noupdate,(iy+rpgflags)
```
Note that tile animation counters will still go, they just won't trigger
re-rendering.

### Dialog

### Text

#### Rectangles

## Events
Events are programmed using a very basic [scripting language](#scripting).

* Kinds of events

### Scripting
