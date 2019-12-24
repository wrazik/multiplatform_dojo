# Known bugs

1. State update doesn't work as expected post animation.
2. Rotations have tendency to slide (have to take center offset into account to work properly).

# Things missing

1. Fire animation and bullet state representation.
2. Controller with networking support.
3. Networked dummy AI.
4. Initial orientation of a tank is not configurable at the moment.
5. Map is always assumed to be square.
6. Collisions have to be added.

# Refactoring needed

1. The way responsibilities are divided between Player and Tank needs to be redone.
2. Some properties should be hidden.
