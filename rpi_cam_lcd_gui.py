#!/usr/bin/python3
# Display captured images and status from RPi NoIR Camera in GUI and LCD
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 12.12.2020.
# Repo: https://github.com/etfovac/rpi_cam/
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, NoIR Camera module, LCD 16x2

import tkinter
import cam_gui
import lcd_1602

LCD_ref = lcd_1602.LCD()
LCD_ref.printout_threads_start()
LCD_ref.keyboard_listener_start()

class GUI(cam_gui.CamGUI):
    def UpdateStatusStrip(self,line):
        self.statusStrip.set(line)
        self.root.update()
        LCD_ref.status = self.statusStrip.get()
        LCD_ref.event_print.set()

rpi_gui = GUI("RPi: IR Camera + LCD")
rpi_gui.start()

# * END