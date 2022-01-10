
import time
from asyncio.tasks import Task
from base import *



class Shimen(Base):
    EventLingqu=Event('./pic/shimen/lingqu.png',RECTS.Task)
    EventShimenRenwu=Event('./pic/shimen/shimen_renwu.png',RECTS.Task)
    EventQuwancheng=Event('./pic/shimen/quwancheng.png',RECTS.BottomHalf)
    EventXuanzeyaozuodeshi=Event('./pic/shimen/xuanzeyaozuodeshi.png',RECTS.RightHalf)
    EventShicha=Event('./pic/shimen/shicha.png',RECTS.RightHalf)

    def run(self):

        #领取师门任务
        pos = self.EventLingqu.find(self.image())
        if pos:
            self.Lingqu(pos)
        elif self.EventShimenRenwu.find(self.image()):
            self.EventShimenRenwu.click(self)

        self.doing()

    def Lingqu(self,pos):
        #点击任务栏师门任务
        self.click(pos[0],pos[1])
        time.sleep(0.5)

        pos = self.EventQuwancheng.find(self.screenShot())
        if pos:
            self.click(pos[0],pos[1])
    
    def doing(self):
        pos = self.EventXuanzeyaozuodeshi.find(self.screenShot())
        if pos:
            self.ShichaRenwu(pos)
    
    def ShichaRenwu(self,pos):
        if self.EventShicha.find(self.image()):
            self.click(self)



task=Shimen()
task.run()