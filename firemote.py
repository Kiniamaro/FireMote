# VERSION 0.1
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

button_delay = 0.2
time_then = 0;
mouse_mode = False

button_actions = {
    cwiid.BTN_B + cwiid.BTN_UP       : (uinput.KEY_UP),
    cwiid.BTN_B + cwiid.BTN_DOWN     : (uinput.KEY_DOWN),
    cwiid.BTN_B + cwiid.BTN_LEFT     : (uinput.KEY_LEFT),
    cwiid.BTN_B + cwiid.BTN_RIGHT    : (uinput.KEY_RIGHT),
    cwiid.BTN_B + cwiid.BTN_A        : ('SAVE'),
    cwiid.BTN_UP                     : (uinput.KEY_LEFTCTRL, uinput.KEY_EQUAL),
    cwiid.BTN_DOWN                   : (uinput.KEY_LEFTCTRL, uinput.KEY_MINUS),
    cwiid.BTN_LEFT                   : (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEUP),
    cwiid.BTN_RIGHT                  : (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEDOWN),
    cwiid.BTN_PLUS + cwiid.BTN_MINUS : ('QUIT'),
    cwiid.BTN_A                      : (uinput.BTN_MIDDLE),
    cwiid.BTN_HOME                   : ('MOUSE')
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
                uinput.REL_Y])

# checks battery life and turn on lights
# according to the battery life (4 lights being > 80% and 0 lights being < 20% )                
def get_battery_life(wiimote) : 
    max_life = cwiid.BATTERY_MAX
    percent_left = int(100.0 * wiimote.state['battery'] / max_life)
    
    if (percent_left >= 80) : 
        led = 15 # 4 lights
    elif (percent_left >= 60) :
        led = 7 # 3 lights
    elif (percent_left >= 40) :
        led = 3 # 2 lights
    elif (percent_left >= 20) :
        led = 1 # 1 light
    else :
        led = 16 # no light
    return led

# all button combos
def action(a):
   return button_actions[a]
                
time.sleep(1)
connected = False

while True :

    try:
        wii = cwiid.Wiimote()
        connected = True
    except :
        connected = False
        
    # indicates to the user that the wiimote is connected
    if connected : 
        for i in xrange(0,2):
            wii.rumble = 1
            time.sleep(0.4)
            wii.rumble = 0
            wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
            
            
    # start listening for inputs
    while connected:
        time.sleep(button_delay) # cpu hogging fix
        buttons = wii.state['buttons'] # Sum of the buttons pressed (int)
        
        if ((time.time() * 1000) - 60000 >= time_then) : # checks battery life every minute
            wii.led = get_battery_life(wii)
            time_then = (time.time() * 1000)

        try :
            what_do = action(buttons)
        except KeyError :
            continue

        if what_do != None :
            do_action = True
        else : 
            do_action = False

        if do_action :
            
            # activates mouse mode and changed button_delay so things are faster
            if what_do == 'MOUSE' : 
                mouse_mode = not mouse_mode
                if (mouse_mode) :
                    button_delay = 0.02
                else :
                    button_delay = 0.2
                time.sleep(2)
            
            # Moves the mouse cursor with DPAD when activated, no other input works
            if mouse_mode :
                if buttons == cwiid.BTN_UP : 
                    device.emit(uinput.REL_Y, -5)
                if buttons == cwiid.BTN_DOWN : 
                    device.emit(uinput.REL_Y, 5)
                if buttons == cwiid.BTN_LEFT : 
                    device.emit(uinput.REL_X, -5)
                if buttons == cwiid.BTN_RIGHT : 
                    device.emit(uinput.REL_X, 5)    
            else :
            
                if what_do == "SAVE" :
                    device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_S])
                    time.sleep(0.5)
                    device.emit_click(uinput.KEY_ENTER)
                    time.sleep(1)

                if what_do == "QUIT" :
                    print '\nClosing connection ...'
                    wii.rumble = 1
                    time.sleep(1)
                    wii.rumble = 0
                    wii = None
                    connected = False

                if type(what_do[0]) == int :
                    device.emit_click(what_do)

                elif type(what_do[0]) == tuple :
                    device.emit_combo(what_do)
              
