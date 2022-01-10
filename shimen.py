
import time
from asyncio.tasks import Task
from base import *



class Shimen(Base):
    EventLingqu=Event('./pic/shimen/lingqu.png',RECTS.Task)
    EventShimenRenwu=Event('./pic/shimen/shimen_renwu.png',RECTS.Task)
    EventQuwancheng=Event('./pic/shimen/quwancheng.png',RECTS.BottomHalf)
    EventShicha=Event('./pic/shimen/shicha.png',RECTS.RightHalf)

    def run(self):

        #领取师门任务
        if self.find(self.EventLingqu):
            self.Lingqu(self.EventLingqu.Position())
        elif self.find(self.EventShimenRenwu):
            self.click(self.EventShimenRenwu.Position())

        self.doing()

    def Lingqu(self,pos):
        #点击任务栏师门任务
        self.click(pos[0],pos[1])
        time.sleep(0.5)

        if self.findFromNow(self.EventQuwancheng):
            self.click(self.EventQuwancheng.Position())
    
    def doing(self):
        self.waitRun()
        event=self.TaskType()
        if event.EvenType==XUAN_ZE_DO:
            self.XuanZeTask(event.Position())
    
    def XuanZeTask(self,pos):
        if self.find(self.EventShicha):
            #找到有关师门的按钮
            self.click(self.EventShicha.Position())
        else:
            #未找到有关师门的按钮，选择第一个
            self.click(pos[0]+154,pos[1]+92)



task=Shimen()
task.run()