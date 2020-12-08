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


class CamGUI(tkinter.Frame):
    def __init__(self,parent):
        self.parent = parent
        self.prop = Prop()
        tkinter.Frame.__init__(self,self.parent)
        self.previewUpate = tkinter.IntVar()
        self.statusStrip = tkinter.StringVar()
        self.canvas = tkinter.Canvas(self.parent,
                                     width=self.prop.szt.PreviewSize[0],
                                     height=self.prop.szt.PreviewSize[1])
        self.canvas.grid(row=0,columnspan=4)
        self.CaptureBtn = tkinter.Button(self.parent,text="Capture",
                                        command = self.Capture)
        self.CaptureBtn.grid(row=1,column=0)
        self.previewChk = tkinter.Checkbutton(self.parent,text="Preview",
                                         variable=self.previewUpate)
        self.previewChk.grid(row=1,column=1)
        self.StatusStripLabel = tkinter.Label(self.parent,
                                      textvariable=self.statusStrip)
        self.StatusStripLabel.grid(row=2,column=0,columnspan=3)
        self.CaptureStillPreview()

    def CamCapture(self,filename,size=Prop.szt.FullSize):
        with picamera.PiCamera() as cam:
            cam.resolution = size
            print('Image: {0}'.format(filename))
            # TODO: add time measurement for capture
            # TODO: change folder, browse from GUI
            cam.capture(filename)
            
    def GetPhotoImage(self,filename,previewsize=Prop.szt.NoReSize):
        encoding = Encoding(filename)
        print('Image encoding: {0}'.format(encoding))
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
                print(errlog)
        return TK_PhotoImage
            
    def TStamp(self):
        tstring=datetime.datetime.fromtimestamp(time.time())
        return tstring.strftime("%Y%m%d_%H%M%S")

    def UpdateStatusStrip(self,text):
        self.statusStrip.set(text)
        self.update()

    def Capture(self):
        """Captures an image on RPi PiCamera, saves it to file and displays it.
            If 'Preview' is checked, overwrites a preview file.
            If not, saves to new file and overwrites a preview file.
        """
        self.CaptureBtn["state"] = "disabled"
        self.UpdateStatusStrip("Capturing...")
        self.update()
        if self.previewUpate.get()==1:
            self.CaptureStillPreview()
        else:
            self.CaptureStill()
        self.CaptureBtn["state"] = "active"

    def CaptureStill(self):
        name = self.TStamp()+self.prop.imt.PNG
        self.CamCapture(name,self.prop.szt.FullSize)
        self.UpdatePreview(name,self.prop.szt.PreviewSize)
        self.UpdateStatusStrip(name)

    def CaptureStillPreview(self):
        self.CamCapture(self.prop.PreviewFile,self.prop.szt.PreviewSize)
        self.UpdatePreview(self.prop.PreviewFile)
        self.UpdateStatusStrip(self.prop.PreviewFile)

    def UpdatePreview(self,filename,previewsize=Prop.szt.NoReSize):
        self.UpdateStatusStrip("Loading Preview...")
        self.DispImage = self.GetPhotoImage(filename,previewsize)
        self.TK_Image = self.canvas.create_image(0,0,
                                               anchor=tkinter.NW,
                                               image=self.DispImage)
        self.update()

    # END
    