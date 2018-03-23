class MyButton():
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
    def setImage(self,image):
        self.image = image
    def getImage(self):
        return self.image
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWithin(self,mx,my):
        if mx >= self.x and mx <= self.x + self.image.get_width():
            if my >= self.y and my <= self.y +self.image.get_height():
                return True
        return False
