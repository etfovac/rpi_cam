# Display RPi info on a monochromatic character LCD
# Version:  v2.0
# Author: Nikola Jovanovic
# Date: 09.12.2020.
# Repo: https://github.com/etfovac/rpi_lcd
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, LCD 1602 module (HD44780, 5V, Blue backlight, 
# 16 chars, 2 lines), Bi-Polar NPN Transistor (2N3904 or eq)

# https://learn.adafruit.com/character-lcds/python-circuitpython
# https://www.mbtechworks.com/projects/drive-an-lcd-16x2-display-with-raspberry-pi.html
# https://www.rototron.info/using-an-lcd-display-with-inputs-interrupts-on-raspberry-pi/
# https://www.rototron.info/lcd-display-tutorial-for-raspberry-pi/#downloads
# https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
# https://www.elprocus.com/lcd-16x2-pin-configuration-and-its-working/
# https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/python-code
# https://bogotobogo.com/python/Multithread/python_multithreading_Event_Objects_between_Threads.php
# https://pypi.org/project/pynput/
# https://components101.com/transistors/bc548-npn-transistor

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep
import signal
import threading
from pynput import keyboard
import sys
import os
sys.path.append(os.path.abspath(".."))
import config.printout_info as cpi
import config.printout_format as cpf

class LCD():
    def __init__(self, lcd_columns=16, lcd_rows=2):
        # Raspberry Pi Pin Config:
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d7 = digitalio.DigitalInOut(board.D13)
        lcd_d6 = digitalio.DigitalInOut(board.D6)
        lcd_d5 = digitalio.DigitalInOut(board.D5)
        lcd_d4 = digitalio.DigitalInOut(board.D22)
        lcd_backlight = digitalio.DigitalInOut(board.D27)
        # a NPN transistor's Base switches the LED backlight on/off
        
        # Init lcd class obj
        self.LCD = characterlcd.Character_LCD_Mono(
            lcd_rs, lcd_en,
            lcd_d4, lcd_d5, lcd_d6, lcd_d7,
            lcd_columns, lcd_rows, lcd_backlight
        )
        self.LCD.text_direction = self.LCD.LEFT_TO_RIGHT
        self.LCD.backlight = True
        self.LCD.clear()
        self.LCD.blink = True
        self.lcd_msg("<Setup>...")
        self.LCD.cursor = True
        
        self.msg_list = cpi.lcd_msg_list(lcd_columns, lcd_rows)

        self.printout_threads_setup([1,6])
        self.keyboard_listener_setup()


    def lcd_msg(self, msg):
        """Prints msg_str to terminal and LCD.
        LCD is first cleared.
        Args:
            msg (string): string formatted by printout_format.py into 2 rows of 16 chars
        """
        self.LCD.clear()
        sleep(0.1)
        self.LCD.message = msg
        print(msg)

    def lcd_printout(self, ix, delay):

        for msg in self.msg_list[ix]:
            self.lcd_msg(msg)
            sleep(delay)

    def lcd_printout_timeout(self, end_event, event, timeout_sec=1):
        # Triggered on event timeout
        cntr = 0
        while (not event.isSet()) and (not end_event.isSet()):
            
            cntr += cntr
            # print(cntr) #=0 => e.wait works
            event_is_set = event.wait(timeout_sec)
            if end_event.isSet(): break
            if event_is_set:
                self.lcd_printout(0,1.5)
                event.clear()  # clear isSet flag in event
            else:
                self.lcd_msg(cpf.msg_form(cpi.lcd_timestamp()[0:2]))

            
    def lcd_printout_timeout2(self, end_event, event, timeout_sec=6):
        # Triggered on event timeout
        while (not event.isSet()) and (not end_event.isSet()):
            
            event_is_set = event.wait(timeout_sec)
            if end_event.isSet(): break
            if not(event_is_set):  # periodic remainder
                self.lcd_printout(1,3)

    def on_press(self,key):
        # Keyboard interupt triggers thread event:
        if key == keyboard.Key.insert:
            self.lcd_event_print.set()

    #     try:
    #         print('alphanumeric key {0} pressed'.format(key.char))
    #     except AttributeError:
    #         print('special key {0} pressed'.format(key))

    def on_release(self,key):
        if key == keyboard.Key.esc:
            print('{0} released - Stopping the keyboard listener'.format(key))
            return False
        if key == keyboard.Key.end:
            self.end()
            return False

    def printout_threads_setup(self, timeout_sec=[1,6]):
        self.lcd_event_print = threading.Event()
        self.lcd_event_print2 = threading.Event()
        self.lcd_event_end = threading.Event()
        #lcd_thread = threading.Thread(target=lcd_printout, args=())
        #lcd_thread.start()
        self.lcd_thread = threading.Thread(name='non-blocking P1',
                                    target = self.lcd_printout_timeout,
                                    args = (self.lcd_event_end, self.lcd_event_print,
                                            timeout_sec[0]))
        self.lcd_thread2 = threading.Thread(name='non-blocking P2',
                                    target=self.lcd_printout_timeout2,
                                    args=(self.lcd_event_end, self.lcd_event_print2,
                                          timeout_sec[1]))

    def printout_threads_start(self):
        self.lcd_thread.start()
        self.lcd_thread2.start()

    def keyboard_listener_setup(self):
        self.listener = keyboard.Listener(on_press = self.on_press,
                                          on_release = self.on_release)

    def keyboard_listener_start(self):
        self.listener.start()
        self.listener.wait()

    def end(self):
        self.listener.stop()
        self.lcd_event_end.set()  # Send End event to LCD printouts
        self.lcd_thread.join()
        self.lcd_thread2.join()
        self.LCD.backlight = False  # Turns off the LED backlight
        sys.exit(0)

        
def main():
    LCD_ref = LCD()
    LCD_ref.printout_threads_start()
    LCD_ref.keyboard_listener_start()
  
if __name__ == "__main__":
    main()   
