from utils import *

XUAN_ZE_DO = 1
ZHAN_DOU=2
SHI_YONG=3
GOU_MAI=4
        

class Base(Device):
    EventHuodong=Event('./pic/base/huodong.png',RECTS.TopHalf)
    EventZhiyin=Event('./pic/base/zhiyin.png',RECTS.TopHalf)
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
        # print('查找',self.EventZhiyin.file)
        # lx, ly, rx, ry=self.EventZhiyin.Rect
        # cv2.imshow('image.png',self.image())

        # cv2.imshow('rect.png',self.image()[ly: ry, lx: rx])
        # cv2.imshow('zhiyin.png',self.EventZhiyin.Img)
        # cv2.waitKey(0)
        # if self.find(self.EventZhiyin,0.6):
        #     print('找到',self.EventZhiyin.file)
        #     print(self.EventZhiyin.Position())
        if self.find(self.EventHuodong) or self.find(self.EventZhiyin):
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
        elif self.find(self.EventJixiBtn,0.9):
            print('跳过剧情')
            self.click(*self.EventJixiBtn.Position())
            
        
    def Begin(self):
        while not self.isHomePage():
            for event in self.EventBeginCancel:
                if self.find(event):
                    self.click(*event.Position)
                    time.sleep(0.2)
                    self.flush()