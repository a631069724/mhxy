
import uiautomator2 as u2
import cv2
import numpy as np
import random
import time
from enum import Enum

XUAN_ZE_DO = 1
ZHAN_DOU=2
SHI_YONG=3
GOU_MAI=4
        

class RECTS(object):
    Task=(1028,108,1280,512)
    BottomHalf=(0,360,1280,720)
    RightHalf=(640,0,1280,720)
    TopHalf=(0,0,1280,360)

def imgRead(file):
    return cv2.imread(file,0)


def matchRect(img, template, rect, threshold = 0.8):
        lx, ly, rx, ry = rect
        rect_img = img[ly: ry, lx: rx]
        res = cv2.matchTemplate(rect_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        locs = zip(*loc[::-1])
        for pt in locs:
            return pt[0]+lx,pt[1]+ly
        return None
    

def match(img1,img2):
    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= 0.8)
    locs = zip(*loc[::-1])
    for pt in locs:
        return pt
    return None



class Device():
    d=u2.connect('127.0.0.1:7555')
    _h,_w=d.window_size()
    _widthScale=1280/_w
    _heightScale=720/_h
    _wScale=_w/1280
    _hScale=_h/720
    img=None

    def __init__(self) -> None:
        self.img=self.screenShot()
        

    def screenShot(self):
        self.img=self.d.screenshot()
        screen=cv2.cvtColor(np.array(self.img), cv2.COLOR_BGR2GRAY)
        size=screen.shape
        self.img = cv2.resize(screen,(int(size[1]*self._widthScale),int(size[0]*self._heightScale)),interpolation= cv2.INTER_LINEAR)
        # cv2.imshow('screen.png',self.img)
        # cv2.waitKey(0)
        return self.img

    def click(self,x,y):
        rx = (int(x) + random.randint(0, 10))*self._wScale
        ry = (int(y) + random.randint(0, 10))*self._hScale
        self.d.click(rx,ry)
    
    def image(self):
        return self.img
    
    def showImage(self,img):
        cv2.imshow('image.png',img)
        cv2.waitKey(0)

    def find(self,event, threshold = 0.8):
        event.Pos = matchRect(self.image(),
            event.Img,
            event.Rect,
            threshold=threshold)
        return event.Pos

    def flush(self):
        self.screenShot()

    def isCmpare(self,img1,img2):
        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= 0.8)
        locs = zip(*loc[::-1])

        for pt in locs:
            return True
        return False

    def findFromNow(self,event):
        #耗时尽量少用
        event.Pos = matchRect(self.screenShot(),
            event.Img,
            event.Rect)
        return event.Pos
    
    

class Event():
    def __init__(self,file,RECT) -> None:

        self.file=file
        self.Img=None
        self.Pos=tuple
        self.EvnType=None
        self.Rect=RECT
        if file is not '':
            self.Img=imgRead(file)
        else:
            return
        if self.Img is None:
            print('图片:',self.file,'未找到')
        

    def Position(self):
        return self.Pos


class Base(Device):
    EventHuodong=Event('./pic/base/huodong.png',RECTS.TopHalf)
    EventShiyong=Event('./pic/base/shiyong.png',RECTS.RightHalf)
    EventGuajiQuxiao=Event('./pic/base/guaji_quxiao.png',RECTS.BottomHalf)
    EventXuanzeyaozuodeshi=Event('./pic/base/xuanzeyaozuodeshi.png',RECTS.RightHalf)
    EventBaitan=Event('./pic/base/baitan.png',RECTS.TopHalf)
    EventZidong=Event('./pic/base/zidong.png',RECTS.BottomHalf)
    EventGoumai=Event('./pic/base/goumai.png',RECTS.BottomHalf)
    EventGoumai2=Event('./pic/base/goumai2.png',RECTS.BottomHalf)
    EventGoumaiXuqiu=Event('./pic/base/goumai_xuqiu.png',RECTS.TopHalf)
    EventShangjiao=Event('./pic/base/shangjiao.png',RECTS.BottomHalf)
    EventJixiBtn=Event('./pic/base/jixu_btn.png',RECTS.TopHalf)
    EventBeginCancel=[
        Event('./pic/base/begin_guanbi1.png',RECTS.RightHalf),
        Event('./pic/base/begin_guanbi2.png',RECTS.RightHalf),
    ]
    def waitRun(self):
        while True:
            if self.isHomePage():
                img1=self.screenShot()[60:80,149:202]
                time.sleep(0.5)
                img2=self.screenShot()[60:80,149:202]
                if self.isCmpare(img1,img2):
                    break
                else:
                    print('跑图中...')
            else:
                break

    def waitFight(self):
        print('战斗中...')
        if self.find(self.EventZidong):
            self.click(*self.EventZidong.Position())
            time.sleep(0.2)
        while self.findFromNow(self.EventGuajiQuxiao):
            time.sleep(2)

    def isHomePage(self): 
        if self.find(self.EventHuodong):
            return True
        return False
    
    def TaskType(self):
        if self.find(self.EventXuanzeyaozuodeshi):
            self.EventXuanzeyaozuodeshi.EvnType=XUAN_ZE_DO
            return self.EventXuanzeyaozuodeshi
        elif self.find(self.EventGuajiQuxiao):
            self.EventGuajiQuxiao.EvnType=ZHAN_DOU
            return self.EventGuajiQuxiao
        # elif self.find(self.EventShiyong):
        #     self.EventShiyong.EvnType=SHI_YONG
        #     return self.EventShiyong
        # elif self.find(self.EventBaitan):
        #     self.EventBaitan.EvnType=GOU_MAI
        #     return self.EventBaitan
        return Event('',())
    
    def BaseRun(self):
        #使用
        if self.find(self.EventShiyong):
            print('使用物品')
            self.click(*self.EventShiyong.Position())
        elif self.find(self.EventGoumai):
        #购买1
            print('购买物品')
            if self.find(self.EventGoumaiXuqiu):
                self.click(*self.EventGoumaiXuqiu.Position())
            self.click(*self.EventGoumai.Position())
        elif  self.find(self.EventGoumai2):
        #购买2
            print('购买物品')
            if self.find(self.EventGoumaiXuqiu):
                    self.click(*self.EventGoumaiXuqiu.Position())
            self.click(*self.EventGoumai2.Position())
        elif self.find(self.EventShangjiao):
        #上交
            print('上交物品')
            self.click(*self.EventShangjiao.Position())
        #TODO 跳过剧情
        elif self.find(self.EventJixiBtn):
            print('跳过剧情')
            self.click(*self.EventJixiBtn.Position())
            
        
    def Begin(self):
        while not self.isHomePage():
            for event in self.EventBeginCancel:
                if self.find(event):
                    self.click(*event.Position)
                    self.flush()