from base import *
import cv2

class MyWork(Base):
    EventGoumai=Event('./pic/shimen/goumai.png',RECTS.BottomHalf)
    def run(self):
        # cv2.imshow('1.png',self.EventGoumai.Img)
        # cv2.waitKey(0)
        # print(self.EventGoumai.Img)
        self.showImage(self.EventGoumai.Img)
    
MyWork().run()