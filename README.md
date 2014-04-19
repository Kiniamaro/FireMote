# FireMote

a simple script to translate wiimote inputs to keyboard shortcuts for firefox

## Dependencies

+ cwiid
+ Python cwiid (pip should work)
+ uinput ([tuomasjjrasanen/python-uinput](https://github.com/tuomasjjrasanen/python-uinput))

## Changelog

**V0.1**
  - Added mouse_mode
  - A button for middle mouse click

## Controls

```
1 + 2 --> connect wiimote (doesn't work with the new wiimote plus, use sync button instead)
PLUS + MINUS --> disconnect wiimote
DPAD_LEFT --> change tab
DPAD_RIGHT --> change tab
DPAD_UP --> zoom in
DPAD_DOWN --> zoom out
B + DPAD --> arrow keys
B + A --> save page
A   --> Middle Mouse click
HOME --> Toggles mouse mode

MOUSE_MODE :

  DPAD --> Move mouse
```
## TODO

+ better implement mouse_mode
+ Make things prettier
