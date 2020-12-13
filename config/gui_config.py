
class ImgType():
    def __init__(self):
        self.PNG = ".png"
        self.JPEG = ".jpg"
        self.GIF = ".gif"
        self.PPM = ".ppm"

class ImgSize(object):
    def __init__(self, 
                 psize=(320,240), 
                 fsize=(2592,1944), 
                 msize=(1920,1080), 
                 none=(0,0)):
        self.PreviewSize = psize
        self.FullSize = fsize
        self.MediumSize = msize
        self.NoReSize = none

def Encoding(imgfile):
    return str.split(imgfile,".")[1].lower()
   
class Prop():
    szt = ImgSize()
    imt = ImgType()
    PreviewFile = "temp"+imt.GIF
    TempFile = "temp"+imt.PPM
    SaveFileType = imt.PNG
    SaveImageType = Encoding(SaveFileType)
