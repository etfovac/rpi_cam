#!/usr/bin/python3
# Display captured images and status from RPi NoIR Camera in GUI and LCD
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 12.12.2020.
# Repo: https://github.com/etfovac/rpi_cam/
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, NoIR Camera module, LCD 16x2

import cam_gui
import lcd_1602

class GUI(cam_gui.CamGUI):
    def __init__(self, title):
        # order matters
        self.LCD_ref = lcd_1602.LCD()
        super().__init__(title)
        
    def UpdateStatusStrip(self,line):
        self.LCD_ref.status = super().UpdateStatusStrip(line)
        self.LCD_ref.event_print.set()
        
    def start(self):
        # order matters
        self.LCD_ref.printout_threads_start()
        self.LCD_ref.keyboard_listener_start()
        super().start()

    def stop(self):
        super().stop()
        self.LCD_ref.event_end.set()

def main():
    rpi_gui = GUI("RPi: IR Camera + LCD")
    rpi_gui.start()
    
if __name__ == "__main__":
    main()
    
# * END