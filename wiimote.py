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
        pressed = False # only one command can be registered per loop
        
        #can also be (buttons & cwiid.BTN_B & cwiid.BTN_UP & pressed == False)
        if (buttons - cwiid.BTN_B - cwiid.BTN_UP == 0 and pressed == False):
            device.emit_click(uinput.KEY_UP)
            time.sleep(button_delay)
            pressed = True

        if (buttons - cwiid.BTN_B - cwiid.BTN_DOWN == 0 and pressed == False):
            device.emit_click(uinput.KEY_DOWN)
            time.sleep(button_delay)
            pressed = True

        if (buttons - cwiid.BTN_B - cwiid.BTN_LEFT == 0 and pressed == False):
            device.emit_click(uinput.KEY_LEFT)
            time.sleep(button_delay)
            pressed = True
            
        if (buttons - cwiid.BTN_B - cwiid.BTN_RIGHT == 0 and pressed == False):
            device.emit_click(uinput.KEY_RIGHT)
            time.sleep(button_delay)
            pressed = True
        
        #disconects the current wiimote and starts looking for a new connection again
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0 and pressed == False):
            print '\nClosing connection ...'
            wii.rumble = 1
            time.sleep(1)
            wii.rumble = 0
            wii = None
            pressed = True
            connected = False       

        if (buttons - cwiid.BTN_A - cwiid.BTN_B == 0  and pressed == False):
           # print "this button works"
            device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_S])
            time.sleep(0.5)
            device.emit_click(uinput.KEY_ENTER)
            time.sleep(1)
            pressed = True

        if (buttons & cwiid.BTN_LEFT and pressed == False):
            print 'Left pressed'
            device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_PAGEUP])
            time.sleep(button_delay)
            pressed = True

        if(buttons & cwiid.BTN_RIGHT and pressed == False):
            print 'Right pressed'
            device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_PAGEDOWN])
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_UP and pressed == False):
            device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_EQUAL])
            print 'Up pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_DOWN and pressed == False):
            device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_MINUS])
            print 'Down pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_1 and pressed == False):
            print 'Button 1 pressed'   
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_2 and pressed == False):
            print 'Button 2 pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_A and pressed == False):
            print 'Button A pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_B and pressed == False):
            print 'Button B pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_HOME and pressed == False):
            print 'Button HOME pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_MINUS and pressed == False):
            print 'Minus Button pressed'
            time.sleep(button_delay)
            pressed = True

        if (buttons & cwiid.BTN_PLUS and pressed == False):
            print 'Plus Button pressed'
            time.sleep(button_delay)
            pressed = True

        
        #sleeps so we don't hog the CPU      
        if not pressed :
            time.sleep(button_delay)


