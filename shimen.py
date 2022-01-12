
import time
from asyncio.tasks import Task
from base import *
import _thread


class Shimen(Base):
    ShiMenDetail=None
    PrePosition=None
    EventLingqu=Event('./pic/shimen/lingqu.png',RECTS.Task)
    EventShimenRenwu=Event('./pic/shimen/shimen_renwu.png',RECTS.Task)
    EventQuwancheng=Event('./pic/shimen/quwancheng.png',RECTS.BottomHalf)
    EventXuanze=Event('./pic/shimen/xuanze.png',RECTS.BottomHalf)
    EventShicha=Event('./pic/shimen/shicha.png',RECTS.RightHalf)
    EventXuanzeDaan=Event('./pic/shimen/xuanze_daan.png',RECTS.RightHalf) 
    EventShiMenDone=Event('./pic/shimen/done.png',RECTS.RightHalf) 
    
    
    EventWenDa={
        Event('./pic/shimen/wenda_qs_dazao.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_dazao.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_shimengeshu.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_shimen20.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_chuandai.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_chuandai.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_sanjie.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_sanjie.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_huaguojineng.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_huaguojineng.png',RECTS.RightHalf)
        }

    def AutoScreenShot(self):
        while True:
            self.screenShot()
            time.sleep(0.1)

    def Run(self):
        _thread.start_new_thread(self.AutoScreenShot)
        #起始界面
        self.Begin()
        #领取师门任务
        if self.find(self.EventLingqu):
            self.Lingqu(self.EventLingqu.Position())
        time.sleep(1)
        while not self.isDone():
            self.UseImg() 
            self.doing()
            time.sleep(1)
            self.flush()
        print('师门任务完成')
    
    
    def doing(self):
        event=self.TaskType()
        if event.EvnType==XUAN_ZE_DO:
            self.XuanZeTask(event.Position())
        elif event.EvnType==ZHAN_DOU:
            self.waitFight()
        else:
            self.BaseRun()
            

    def isDone(self):
        #self.flush()
        #同一任务 防止点击频繁被系统判断脚本
        if  self.find(self.EventShimenRenwu):
            if self.ShiMenDetail is None:
                x,y=self.EventShimenRenwu.Position()
                self.ShiMenDetail=Event('',RECTS.RightHalf)
                self.ShiMenDetail.Img=self.image()[y:y+80,x:x+230]
                self.PrePosition=self.image()[60:80,149:202] 
            elif self.findImg(self.ShiMenDetail) and not self.isCmpare(self.PrePosition,self.image()[60:80,149:202]):
                self.PrePosition=self.image()[60:80,149:202] 
                #print('同一任务跳过点击')
                return
            if self.find(self.EventXuanzeyaozuodeshi):
                return
            print('点击任务栏师门任务')
            x,y=self.EventShimenRenwu.Position()
            self.ShiMenDetail.Img=self.image()[y:y+80,x:x+230]
            self.PrePosition=self.image()[60:80,149:202]
            self.click(*self.EventShimenRenwu.Position())
            time.sleep(1)
            return
        if self.find(self.EventShiMenDone):
            x,y=self.EventShiMenDone.Position()
            self.click(x+35,y+30)
            return True
        if  self.find(self.EventShimenRenwu) is None \
                and self.find(self.EventXuanzeyaozuodeshi) is None \
                and self.isHomePage(): 
            return True
        return False

    def Lingqu(self,pos):
        #点击任务栏师门任务
        print('领取师门任务')
        self.UseImg()
        self.click(pos[0],pos[1])
        time.sleep(0.5)
        self.flush()
        if self.find(self.EventQuwancheng):
            self.click(*self.EventQuwancheng.Position())
        elif self.find(self.EventXuanze):
            self.click(*self.EventXuanze.Position())
            

    def XuanZeTask(self,pos):
        print('选择要做的事')
        if self.find(self.EventShicha):
            #找到有关师门的按钮
            print('点击包含师门相关任务')
            self.click(*self.EventShicha.Position())
        else:
            #未找到有关师门的按钮，选择第一个
            print('未找到包含师门相关任务，选择第一个')
            self.click(pos[0]+154,pos[1]+92)
        time.sleep(0.2)
        self.screenShot()
        while self.find(self.EventXuanzeDaan):
            self.wenda()

    def wenda(self):
        print('问答任务')
        for key,value in self.EventWenDa.items():
            if self.find(key) and self.find(value):
                self.click(*value.Position())
                return


task=Shimen()
task.Run()