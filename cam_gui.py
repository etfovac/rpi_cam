#!/usr/bin/python3
#cam_gui.py

import datetime
import subprocess
import time
import tkinter
import picamera
from PIL import Image

class Prop():
     PreviewSize = (320,240)
     FullSize = (2592,1944)
     MediumSize = (1920,1080)
     NoReSize = (0,0)
     PreviewFile = "Preview.gif"
     TempFile = "Preview.ppm"

class CamGUI(tkinter.Frame):
    def Run(self,cmd):
        print("Run: "+cmd)
        subprocess.call([cmd],shell=True)

    def CamCapture(self,filename,size=Prop.FullSize):
        with picamera.PiCamera() as cam:
            cam.resolution = size
            print("Image: %s" %filename)
            cam.capture(filename)
            
    def getTKImage(self,filename,previewsize=Prop.NoReSize):
        encoding=str.split(filename,".")[1].lower()
        print("Image encoding: %s"%encoding)
        try:
            if encoding=="gif" and previewsize==Prop.NoReSize:
                theTKImage=tkinter.PhotoImage(file=filename)
            else:
                imageview=Image.open(filename)
                if previewsize!=Prop.NoReSize:
                    imageview.thumbnail(previewsize,Image.ANTIALIAS)
                imageview.save(Prop.PreviewFile,format="png")
                theTKImage=tkinter.PhotoImage(file=Prop.PreviewFile)
        except IOError:
                print("Unable to get: %s"%filename)
        return theTKImage
            
    def timestamp(self):
        ts=time.time()
        tstring=datetime.datetime.fromtimestamp(ts)
        return tstring.strftime("%Y%m%d_%H%M%S")

    def __init__(self,parent):
        self.parent = parent
        tkinter.Frame.__init__(self,self.parent)
        self.parent.title("Camera GUI")
        self.previewUpate= tkinter.IntVar()
        self.filename = tkinter.StringVar()
        self.canvas = tkinter.Canvas(self.parent,
                                     width=Prop.PreviewSize[0],
                                     height=Prop.PreviewSize[1])
        self.canvas.grid(row=0,columnspan=4)
        self.shutterBtn= tkinter.Button(self.parent,text="Shutter",
                                        command = self.shutter)
        self.shutterBtn.grid(row=1,column=0)
        previewChk = tkinter.Checkbutton(self.parent,text="Preview",
                                         variable=self.previewUpate)
        previewChk.grid(row=1,column=1)
        labelFilename = tkinter.Label(self.parent,
                                      textvariable=self.filename)
        labelFilename.grid(row=2,column=0,columnspan=3)
        self.preview()

    def msg(self,text):
        self.filename.set(text)
        self.update()

    def btnState(self,state):
        self.shutterBtn["state"] = state

    def shutter(self):
        self.btnState("disabled")
        self.msg("Taking photo...")
        self.update()
        if self.previewUpate.get()==1:
            self.preview()
        else:
            self.normal()
        self.btnState("active")

    def normal(self):
        name=CamGUI.timestamp(self)+".png"
        CamGUI.CamCapture(self,name,Prop.FullSize)
        self.updateDisp(name,previewsize=Prop.PreviewSize)
        self.msg(name)

    def preview(self):
        CamGUI.CamCapture(self,Prop.PreviewFile,Prop.PreviewSize)
        self.updateDisp(Prop.PreviewFile)
        self.msg(Prop.PreviewFile)

    def updateDisp(self,filename,previewsize=Prop.NoReSize):
        self.msg("Loading Preview...")
        self.myImage=CamGUI.getTKImage(self,filename,previewsize)
        self.theTKImage=self.canvas.create_image(0,0,
                                               anchor=tkinter.NW,
                                               image=self.myImage)
        self.update()

    def exit(self):
        exit()

    # END
    