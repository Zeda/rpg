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


### Tile animation

### Rendering

### Dialog

### Text

### Primitives

#### Rectangles

## Events
Events are programmed using a very basic [scripting language](#scripting).

* Kinds of events

### Scripting
