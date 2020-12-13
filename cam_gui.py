#!/usr/bin/python3
# Display captured images from RPi NoIR Camera in GUI canvas
# Version:  v1.0
# Author: Nikola Jovanovic
# Date: 03.12.2020.
# Repo: https://github.com/etfovac/rpi_cam
# SW: Python 3.7.3
# HW: Pi Model 3B  V1.2, NoIR Camera module

import sys
import os
import datetime
# import subprocess
import time
import tkinter
import picamera
from PIL import Image
sys.path.append(os.path.abspath(".."))
from config.gui_config import Prop, Encoding


class CamGUI():
    def __init__(self, title):
        self.root = tkinter.Tk()  # tkinter.Frame master/top/root
        self.root.title(title)
        self.prop = Prop()

        self.previewUpate = tkinter.IntVar()
        self.statusStrip = tkinter.StringVar()
        self.canvas = tkinter.Canvas(self.root,
                                     width=self.prop.szt.PreviewSize[0],
                                     height=self.prop.szt.PreviewSize[1])
        self.canvas.grid(row=0,columnspan=4,
                         sticky="w"+"e"+"n"+"s", padx=5, pady=5)
        self.CaptureBtn = tkinter.Button(self.root,text="Capture",
                                        command = self.Capture)
        self.CaptureBtn.grid(row=1,column=0)
        self.previewChk = tkinter.Checkbutton(self.root,text="Preview",
                                         variable=self.previewUpate)
        self.previewChk.grid(row=1,column=1)
        self.StatusStripLabel = tkinter.Label(self.root,
                                      textvariable=self.statusStrip,
                                      anchor="sw",
                                      justify="left")
        self.StatusStripLabel.grid(row=2,column=0,columnspan=4)

        self.CaptureStillPreview()

    def CamCapture(self,filename,size=Prop.szt.FullSize):
        with picamera.PiCamera() as cam:
            cam.resolution = size
            self.UpdateStatusStrip('Cap: {0}'.format(filename))
            # TODO: add time measurement for capture
            # TODO: change folder, browse from GUI
            cam.capture(filename)
            
    def GetPhotoImage(self,filename,previewsize=Prop.szt.NoReSize):
        encoding = Encoding(filename)
        self.UpdateStatusStrip('.{0}'.format(encoding))
        try:
            if encoding==self.prop.imt.GIF and previewsize==self.prop.szt.NoReSize:
                TK_PhotoImage=tkinter.PhotoImage(file=filename)
            else:
                imageview=Image.open(filename)
                if previewsize!=self.prop.szt.NoReSize:
                    imageview.thumbnail(previewsize,Image.ANTIALIAS)
                imageview.save(self.prop.PreviewFile,format=self.prop.SaveImageType)
                TK_PhotoImage=tkinter.PhotoImage(file=self.prop.PreviewFile)
        except IOError as ioe:
                errlog='Unable to get: {0} ({1})'.format(filename, str(ioe))
                self.UpdateStatusStrip(errlog)
        return TK_PhotoImage
            
    def TStamp(self):
        tstring=datetime.datetime.fromtimestamp(time.time())
        return tstring.strftime("%Y%m%d_%H%M%S")

    def UpdateStatusStrip(self,line):
        self.statusStrip.set(line)
        print("Cam: {}".format(self.statusStrip.get()))
        self.root.update()

    def Capture(self):
        """Captures an image on RPi PiCamera, saves it to file and displays it.
            If 'Preview' is checked, overwrites a preview file.
            If not, saves to new file and overwrites a preview file.
        """
        self.CaptureBtn["state"] = "disabled"
        self.UpdateStatusStrip("Capturing...")
        self.root.update()
        if self.previewUpate.get()==1:
            self.CaptureStillPreview()
        else:
            self.CaptureStill()
        self.CaptureBtn["state"] = "active"

    def CaptureStill(self):
        name = self.TStamp()+self.prop.SaveFileType
        self.CamCapture(name,self.prop.szt.FullSize)
        self.UpdatePreview(name,self.prop.szt.PreviewSize)

    def CaptureStillPreview(self):
        self.CamCapture(self.prop.PreviewFile,self.prop.szt.PreviewSize)
        self.UpdatePreview(self.prop.PreviewFile)

    def UpdatePreview(self,filename,previewsize=Prop.szt.NoReSize):
        self.UpdateStatusStrip("Load preview...")
        self.DispImage = self.GetPhotoImage(filename,previewsize)
        self.TK_Image = self.canvas.create_image(0,0,
                                               anchor=tkinter.NW,
                                               image=self.DispImage)
        self.root.update()
        self.UpdateStatusStrip("Preview: {}".format(filename))

    def start(self):
        self.root.mainloop()

def main():
    gui=CamGUI("RPi Camera GUI")
    gui.start()
  
if __name__ == "__main__":
    main()   
    