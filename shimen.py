
import time
from asyncio.tasks import Task
from base import *



class Shimen(Base):
    EventLingqu=Event('./pic/shimen/lingqu.png',RECTS.Task)
    EventShimenRenwu=Event('./pic/shimen/shimen_renwu.png',RECTS.Task)
    EventQuwancheng=Event('./pic/shimen/quwancheng.png',RECTS.BottomHalf)
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

    def run(self):
        self.Begin()
        #领取师门任务
        if self.find(self.EventLingqu):
            self.Lingqu(self.EventLingqu.Position())
        elif self.find(self.EventShimenRenwu):
            print('点击任务栏师门任务')

            x,y=self.EventShimenRenwu.Position()
            self.ShiMenDetail=Event('',RECTS.RightHalf)
            self.ShiMenDetail.Img=self.image()[y:y+80,x:x+230]
            self.LingQuShimenPos=self.image()[60:80,149:202]
            self.click(*self.EventShimenRenwu.Position())
        while not self.isDone():
            time.sleep(0.5)
            self.flush()
            self.doing()
        print('师门任务完成')
    
    
    def doing(self):
        event=self.TaskType()
        if event.EvnType==XUAN_ZE_DO:
            self.XuanZeTask(event.Position())
        elif event.EvnType==ZHAN_DOU:
            self.waitFight()
        else:
            self.BaseRun()
            #同一任务 防止点击频繁被系统判断脚本
            if  self.find(self.EventShimenRenwu):
                if self.find(self.ShiMenDetail) and not self.isCmpare(self.LingQuShimenPos,self.image()[60:80,149:202]):
                    return
                print('点击任务栏师门任务')
                x,y=self.EventShimenRenwu.Position()
                self.ShiMenDetail.Img=self.image()[y:y+80,x:x+230]
                self.LingQuShimenPos=self.image()[60:80,149:202]
                self.click(*self.EventShimenRenwu.Position())

    def isDone(self):
        if self.isHomePage() and  self.find(self.EventShimenRenwu) is None:
            return True
        return False

    def Lingqu(self,pos):
        #点击任务栏师门任务
        print('领取师门任务')

        self.click(pos[0],pos[1])
        time.sleep(0.5)

        if self.findFromNow(self.EventQuwancheng):
            self.click(*self.EventQuwancheng.Position())

    def XuanZeTask(self,pos):
        if self.find(self.EventShicha):
            #找到有关师门的按钮
            self.click(*self.EventShicha.Position())
        else:
            #未找到有关师门的按钮，选择第一个
            self.click(pos[0]+154,pos[1]+92)
        time.sleep(0.2)
        while self.findFromNow(self.EventXuanzeDaan):
            self.wenda()

    def wenda(self):
        for key,value in self.EventWenDa.items():
            if self.find(key) and self.find(value,threshold=0.9):
                self.click(*value.Position())
                return


task=Shimen()
task.run()