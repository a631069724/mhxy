
import time
from asyncio.tasks import Task
from base import *



class Shimen(Base):
    EventLingqu=Event('./pic/shimen/lingqu.png',RECTS.Task)
    EventShimenRenwu=Event('./pic/shimen/shimen_renwu.png',RECTS.Task)
    EventQuwancheng=Event('./pic/shimen/quwancheng.png',RECTS.BottomHalf)
    EventShicha=Event('./pic/shimen/shicha.png',RECTS.RightHalf)
    EventXuanzeDaan=Event('./pic/shimen/xuanze_daan.png',RECTS.RightHalf)
    EventGoumaiXuqiu=Event('./pic/shimen/goumai_xuqiu.png',RECTS.TopHalf)
    EventGoumai=Event('./pic/shimen/goumai.png',RECTS.BottomHalf)
    EventShangjiao=Event('./pic/shimen/shangjiao.png',RECTS.BottomHalf)
    
    
    EventWenDa={
        Event('./pic/shimen/wenda_qs_dazao.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_dazao.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_shimengeshu.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_shimen20.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_chuandai.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_chuandai.png',RECTS.RightHalf),
        Event('./pic/shimen/wenda_qs_sanjie.png',RECTS.BottomHalf):Event('./pic/shimen/wenda_ans_sanjie.png',RECTS.RightHalf)
        }

    def run(self):

        #领取师门任务
        if self.find(self.EventLingqu):
            self.Lingqu(self.EventLingqu.Position())
        elif self.find(self.EventShimenRenwu):
            self.click(*self.EventShimenRenwu.Position())
        self.flush()
        self.doing()

    def Lingqu(self,pos):
        #点击任务栏师门任务
        self.click(pos[0],pos[1])
        time.sleep(0.5)

        if self.findFromNow(self.EventQuwancheng):
            self.click(*self.EventQuwancheng.Position())
    
    def doing(self):
        self.waitRun() #耗时必须优化
        event=self.TaskType()
        if event.EvnType==XUAN_ZE_DO:
            self.XuanZeTask(event.Position())
        if event.EvnType==ZHAN_DOU:
            self.waitFight()
        if event.EvnType==SHI_YONG:
            self.click(*event.Position())
        if event.EvnType==GOU_MAI:
            self.goumaiTask()
        
        if self.find(self.EventShangjiao):
             self.click(*self.EventShangjiao.Position())
        self.waitFight()
        
    def goumaiTask(self):
        if self.find(self.EventGoumaiXuqiu):
            self.click(*self.EventGoumaiXuqiu.Position())
            if self.find(self.EventGoumai):
                self.click(*self.EventGoumai.Position())
        self.flush()
        self.waitRun()
        if self.find(self.EventShangjiao):
             self.click(*self.EventShangjiao.Position())

    def XuanZeTask(self,pos):
        if self.find(self.EventShicha):
            #找到有关师门的按钮
            self.click(*self.EventShicha.Position())
        else:
            #未找到有关师门的按钮，选择第一个
            self.click(pos[0]+154,pos[1]+92)
        time.sleep(0.2)
        if self.findFromNow(self.EventXuanzeDaan):
            self.wenda()

    def wenda(self):
        for key,value in self.EventWenDa.items():
            if self.find(key) and self.find(value,threshold=0.9):
                self.click(*value.Position())
                return


task=Shimen()
task.run()