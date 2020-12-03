#!/usr/bin/python3
# Display captured images from RPi NoIR Camera in GUI canvas of tkinter
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 03.12.2020.
# Repo: https://github.com/etfovac/rpi_cam
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, NoIR Camera module

import tkinter
import cam_gui

root=tkinter.Tk()
root.title("RPi Camera GUI")
root.p
cam=cam_gui.CamGUI(root)
root.mainloop()

# END