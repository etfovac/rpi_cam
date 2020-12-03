#!/usr/bin/python3
#rpi_cam_gui.py

import tkinter
import cam_gui

root=tkinter.Tk()
root.title("RPi Camera GUI")
cam=cam_gui.CamGUI(root)
tkinter.mainloop()

# END