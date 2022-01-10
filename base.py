
import uiautomator2 as u2
import cv2
import numpy as np

d=u2.connect('127.0.0.1:7555')

class RECTS(object):
    Task=()


def match_sub_image_in_rect(img_gray, template, rect, threshold = 0.8):
    
        #template = cv2.imread(imgfile, 0)
        ih,iw=img_gray.shape
        # http://stackoverflow.com/questions/19098104/python-opencv2-cv2-wrapper-get-image-size
        height, width = template.shape
        # http://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python
        lx, ly, rx, ry = rect
        cropped_img_gray = img_gray[ly: ry, lx: rx]
        if ry-ly<height or rx-lx<width:
            print('请重新截图')
            return None
        if ih<ry or iw<rx:
            print('超过图片大小')
            return None
        res = cv2.matchTemplate(cropped_img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)

        locs = zip(*loc[::-1])

        if locs:
            for pt in locs:
                return pt[0]+lx,pt[1]+ly
        return None
    

def match(img1,img2):
    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= 0.8)
    locs = zip(*loc[::-1])
    if locs:
        for pt in locs:
            return pt
    return None



class Device():
    _h,_w=d.window_size()
    _widthScale=1280/_w
    _heightScale=720/_h

    def imgRead(self,file):
        return cv2.imread(file,0)

    def screenShot(self):
        img=d.screenshot()
        screen=cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        size=screen.shape
        return cv2.resize(screen,(int(size[1]*self._widthScale),int(size[0]*self._heightScale)),interpolation= cv2.INTER_LINEAR)


class Base(Device):
    imgShimenRenwu=Device().imgRead('./pic/shimen/shimen_renwu.png')

