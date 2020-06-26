import sys
import platform
import time
import socket
import re
import base64

import usb.core
import usb.util


x_max = 5362
y_max = 762
coord_file = './coords.txt'
x_coord = 0
y_coord = 0

# Protocol command bytes
DOWN    = 0x01 #down is pos
UP      = 0x02 #up is neg
LEFT    = 0x04 #left is pos
RIGHT   = 0x08 #right is neg
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

class usb_launcher():
    def __init__(self):
        setup_usb()
        get_coords()
        self.led_on()
		
    def fire(self,val = 1):
        run_command('fire',val)
		
    def led_on(self):
        led(1)
		
    def led_off(self):
        led(0)
		
    def take_aim(self,x,y):
		move_coords(x,y)
		
    def release(self):
        on_exit()
        self.led_off()
        	
	def right(self,val):
		pass
	def left(self,val):
		pass
	def up(self,val):
		pass
	def down(self,val):
		pass
		
	
		
def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE 
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()



def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)

def get_coords():
    global x_coord
    global y_coord
    try:
        f = open(coord_file, 'r')
        x_coord = int(f.readline())
        y_coord = int(f.readline())
        f.close()
    except:
        x_coord = x_max/2
        y_coord = y_max/2
        send_move(DOWN,y_max+200)
        send_move(LEFT,x_max+200)
        send_move(RIGHT,x_max/2)
        send_move(UP,y_max/2)
        
def on_exit():
    f = open(coord_file,'w')
    f.write(str(x_coord)+'\n')
    f.write(str(y_coord)+'\n')
    f.close()
    
def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command

def move_coords(x,y,pos=''):
    global x_coord
    global y_coord
    if not pos:
        x_move = x-x_coord
        y_move = y-y_coord
    if(x_move>0):
        run_command('left',x_move) 
    else:
        run_command('right',abs(x_move))
    if(y_move>0):
        run_command('down',y_move)
    else:
        run_command('up',abs(y_move))
    x_coord = x
    y_coord = y 
         
def main(args):
    launcher = usb_launcher()
    launcher.take_aim(0,0)
    #launcher.take_aim(x_max/2,y_max/2)
    #launcher.take_aim(4000,675)
    #launcher.fire()
    launcher.release()
'''
    setup_usb()
    get_coord()
    #run_command('fire',1)
    move_coords(0,0)
    move_coords(x_max/2,y_max/2)
    run_command('fire',1)
    on_exit()
'''
    

if __name__ == '__main__':
    main(sys.argv)
