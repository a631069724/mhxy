
from asyncio.tasks import Task
from base import *



class Shimen(Base):
    EventShimenRenwu=Event('../pic/shimen/shimen_renwu.png',Task,(1140,224))

    def run(self):
        pos=match_sub_image_in_rect(self.screenShot(),
            self.EventShimenRenwu.Img,
            self.EventShimenRenwu.Rect)
        #师门任务
        if pos:
            self.click(*self.EventShimenRenwu.Click)