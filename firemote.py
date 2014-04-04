#script made to be run in background that listens for a know wiimote
# and lets it connect to the PC, once connected it acts as
# a keyboard and can simulate keyboard key presses.
#
# designed for an enanched firefox browsing experience.
# but can easly be made into anything.

import cwiid
import time 
import uinput

button_delay = 0.2
#must add the key to the device before using it
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
                uinput.KEY_RIGHT])

#all button combos
def action(a):
        return {
            cwiid.BTN_B + cwiid.BTN_UP      : (uinput.KEY_UP),
            cwiid.BTN_B + cwiid.BTN_DOWN    : (uinput.KEY_DOWN),
            cwiid.BTN_B + cwiid.BTN_LEFT    : (uinput.KEY_LEFT),
            cwiid.BTN_B + cwiid.BTN_RIGHT   : (uinput.KEY_RIGHT),
            cwiid.BTN_B + cwiid.BTN_A       : ("SAVE"),
            cwiid.BTN_UP                    : (uinput.KEY_LEFTCTRL, uinput.KEY_EQUAL),
            cwiid.BTN_DOWN                  : (uinput.KEY_LEFTCTRL, uinput.KEY_MINUS),
            cwiid.BTN_LEFT                  : (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEDOWN),
            cwiid.BTN_RIGHT                 : (uinput.KEY_LEFTCTRL, uinput.KEY_PAGEUP),
            cwiid.BTN_PLUS + cwiid.BTN_MINUS: ("QUIT")
        }[a]
                
time.sleep(1)
connected = False

while True :

    try:
        wii=cwiid.Wiimote()
        connected = True
    except :
        connected = False
        
    #indicates to the user that the wiimote is connected
    if connected : 
        for i in xrange(0,2):
            wii.rumble = 1
            time.sleep(0.4)
            wii.rumble = 0
            wii.rpt_mode = cwiid.RPT_BTN
            
    #start listening for inputs
    while connected:
        
        buttons = wii.state['buttons'] # Sum of the buttons pressed (int)
        
        try :
            whatDo = action(buttons)
        except KeyError :
            continue
        
        if whatDo != None :
            doAction = True
        else : 
            doAction = False
            
        if doAction :
            print whatDo
            print len(whatDo) 
            if whatDo == "SAVE" :
                device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_S])
                time.sleep(0.5)
                device.emit_click(uinput.KEY_ENTER)
                time.sleep(1)
                
            elif whatDo == "QUIT" :
                print '\nClosing connection ...'
                wii.rumble = 1
                time.sleep(1)
                wii.rumble = 0
                wii = None
                connected = False
 
            elif type(whatDo[0]) == int :
                device.emit_click(whatDo)
            
            elif type(whatDo[0]) == tuple :
                 device.emit_combo(whatDo)
            
        time.sleep(button_delay)
        
             
