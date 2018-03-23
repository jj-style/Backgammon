class MyToggleSwitch():
    def __init__(self,on,off,x_pos,y_pos,on_text,off_text):
        self.status = True
        self.OnImage = on
        self.OffImage = off
        self.showImage = self.OnImage
        self.x = x_pos
        self.y = y_pos
        self.OnText = on_text
        self.OffText = off_text

    def setSwitchStatus(self):
        if self.status == True:
            self.status = False
            self.showImage = self.OffImage
        else:
            self.status = True
            self.showImage = self.OnImage
    def getText(self):
        if self.status == True:
            return self.OnText
        return self.OffText
    def getStatus(self):
        return self.status
    def getImage(self):
        return self.showImage
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWithin(self,mx,my):
        if mx >= self.x and mx <= self.x + self.showImage.get_width():
            if my >= self.y and my <= self.y +self.showImage.get_height():
                return True
        return False

class MyToggleSwitchColor(MyToggleSwitch):
    def __init__(self,on,off,x_pos,y_pos,on_text,off_text):
        MyToggleSwitch.__init__(self,on,off,x_pos,y_pos,on_text,off_text)
    def getPieceColor(self):
        if self.status == True:
            return [(0,0,0),(255,255,255)]
        return [(0,0,127),(127,0,0)]
    
