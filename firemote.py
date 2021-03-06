# VERSION 0.3.1
#
# Script made to be run in background that listens for a known wiimote
# and lets it connect to the PC, once connected it acts as
# a keyboard and can simulate keyboard key presses.
#
# designed for an enhanced firefox browsing experience,
# but can easily be made into anything.
import time

import cwiid
import uinput

button_delay = 0.01
time_then = 0
mouse_mode = False
BTN_Z = 1
BTN_C = 2

# needed for the anti key spam 
can_do_action = True 

button_actions = {
    cwiid.BTN_B + cwiid.BTN_UP: (uinput.KEY_LEFTCTRL, uinput.KEY_EQUAL),
    cwiid.BTN_B + cwiid.BTN_DOWN: (uinput.KEY_LEFTCTRL, uinput.KEY_MINUS),
    cwiid.BTN_B + cwiid.BTN_LEFT: (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEUP),
    cwiid.BTN_B + cwiid.BTN_RIGHT: (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEDOWN),
    cwiid.BTN_B + cwiid.BTN_A: ('SAVE'),
    cwiid.BTN_UP: (uinput.KEY_UP),
    cwiid.BTN_DOWN: (uinput.KEY_DOWN),
    cwiid.BTN_LEFT: (uinput.KEY_LEFT),
    cwiid.BTN_RIGHT: (uinput.KEY_RIGHT),
    cwiid.BTN_PLUS + cwiid.BTN_MINUS: ('QUIT'),
    cwiid.BTN_A: (uinput.BTN_MIDDLE),
    BTN_Z: (uinput.BTN_LEFT)
}

# must add the key to the device before using it
device = uinput.Device([
    uinput.KEY_LEFTCTRL,
    uinput.KEY_PAGEUP,
    uinput.KEY_PAGEDOWN,
    uinput.KEY_EQUAL,
    uinput.KEY_MINUS,
    uinput.KEY_S,
    uinput.KEY_ENTER,
    uinput.KEY_UP,
    uinput.KEY_DOWN,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.BTN_MIDDLE,
    uinput.REL_X,
    uinput.REL_Y,
    uinput.BTN_LEFT
])

# checks battery life and turn on lights
# according to the battery life (4 lights being > 80% and 0 lights being < 20%)
def get_battery_life(wiimote):
    max_life = cwiid.BATTERY_MAX
    percent_left = int(100.0 * wiimote.state['battery'] / max_life)

    if (percent_left >= 80):
        led = 15  # 4 lights
    elif (percent_left >= 60):
        led = 7  # 3 lights
    elif (percent_left >= 40):
        led = 3  # 2 lights
    elif (percent_left >= 20):
        led = 1  # 1 light
    else:
        led = 16  # no light
    return led

# all button combos
def action(a):
    return button_actions[a]

# Mouse_mode    
def joystick_to_mouse(x, y):
    mov_x = 0
    mov_y = 0
    
    # basicaly checks if the X is not in the DeadZone
    # and if it isnt tells the mouse to move left or right
    # if X is bigger or smaller than the DeadZone
    # values found by trial and error, too lazy to make
    # proper variables for now.
    if x < 103:
        mov_x = x - 103
    elif x > 143:
        mov_x = x - 143
    
    # Ditto
    if y < 97:
        mov_y = y - 97
    elif y > 157:
        mov_y = y - 157 
    device.emit(uinput.REL_Y, -mov_y / 10)
    device.emit(uinput.REL_X, mov_x / 10)

time.sleep(1)
connected = False

while True:
    try:
        wii = cwiid.Wiimote()
        connected = True
    except:
        connected = False

    # indicates to the user that the wiimote is connected
    if connected:
        for i in xrange(0, 2):
            wii.rumble = 1
            time.sleep(0.4)
            wii.rumble = 0
            wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_EXT

    # start listening for inputs
    while connected:
        time.sleep(button_delay)  # cpu hogging fix
        buttons = wii.state['buttons']  # Sum of the buttons pressed (int)
        nun_buttons = 0 # buttons for the nunchuk
        # checks battery life every minute
        if ((time.time() * 1000) - 60000 >= time_then):
            wii.led = get_battery_life(wii)
            time_then = (time.time() * 1000)
            
        try:
            nunchuk = wii.state['nunchuk']['stick']
            nun_buttons = wii.state['nunchuk']['buttons']
        except:
            nunchuk = None

        try:
            what_do = action(buttons + nun_buttons)
        except KeyError:
            what_do = 'NONE'
        
        do_action = False
        if what_do is not 'NONE':
            if can_do_action:
                do_action = True
                can_do_action = False
        else:
            can_do_action = True

        if do_action:

            if what_do == "SAVE":
                device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_S])
                time.sleep(0.5)
                device.emit_click(uinput.KEY_ENTER)
                time.sleep(1)

            if what_do == "QUIT":
                print '\nClosing connection ...'
                wii.rumble = 1
                time.sleep(1)
                wii.rumble = 0
                wii = None
                connected = False

            if type(what_do[0]) == int:
                device.emit_click(what_do)

            elif type(what_do[0]) == tuple:
                device.emit_combo(what_do)
         
        # Nunchuk support, Real Mouse mode
        if nunchuk:
            # tupple with coordinates, (x, y)
            joystick = nunchuk
            joystick_to_mouse(joystick[0], joystick[1]) 

         
         
