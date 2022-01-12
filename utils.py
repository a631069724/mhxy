import uiautomator2 as u2
import cv2
import numpy as np
import random
import time
import threading
from matplotlib import pyplot as plt


lock=threading.Lock()

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

def Rotation(img,angle=90):

    height, width = img.shape[:2]
    
    matRotate = cv2.getRotationMatrix2D((height * 0.5, width * 0.5), angle, 1)
    dst = cv2.warpAffine(img, matRotate, (width, height*2))
    rows, cols = dst.shape[:2]
    
    for col in range(0, cols):
        if dst[:, col].any():
            left = col
            break
    
    for col in range(cols-1, 0, -1):
        if dst[:, col].any():
            right = col
            break
    
    for row in range(0, rows):
        if dst[row,:].any():
            up = row
            break
    
    for row in range(rows-1,0,-1):
        if dst[row,:].any():
            down = row
            break
    
    res_widths = abs(right - left)
    res_heights = abs(down - up)
    res = np.zeros([res_heights ,res_widths, 3], np.uint8)
    
    for res_width in range(res_widths):
        for res_height in range(res_heights):
            res[res_height, res_width] = dst[up+res_height, left+res_width]
    return res

# def flann_match(img,template,rect,threshold=0.7):
#     lx, ly, rx, ry = rect
#     rect_img = img[ly: ry, lx: rx]
    
#     #sift = cv2.xfeatures2d.SIFT_create(30000)
#     sift = cv2.xfeatures2d.SURF_create(300)

#     kp1, des1 = sift.detectAndCompute(template,None)
#     kp2, des2 = sift.detectAndCompute(rect_img,None)
#     FLANN_INDEX_KDTREE = 0
#     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#     #search_params = dict(checks = 50)
#     flann = cv2.FlannBasedMatcher(index_params, {})
#     matches = flann.knnMatch(des1,des2,k=2)
#     good = []
#     for m,n in matches:
#         if m.distance < threshold*n.distance:
#             good.append(m)

#     # #           debug start
#     cv2.imshow('img.png',rect_img)
#     cv2.imshow('template.png',template)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     # #           debug end

#     if len(good)>1:
#         # 获取关键点的坐标
#         src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#         dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
#         mypt=kp2[m.trainIdx].pt
#         print(mypt)
#         #计算变换矩阵和MASK
#         M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
#         matchesMask = mask.ravel().tolist()
#         h,w = template.shape
#         # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
#         pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#         dst = cv2.perspectiveTransform(pts, M)
#         pos=np.int32(dst)[0][0]

#         ##           debug start
#         draw_params = dict(matchColor=(0,255,0), 
#                    singlePointColor=None,
#                    matchesMask=matchesMask, 
#                    flags=2)
#         result = cv2.drawMatches(template,kp1,rect_img,kp2,good,None,**draw_params)
#         cv2.imshow('gray.png',result)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#         ##           debug end

#         #print(pos[0]+lx,pos[1]+ly)
#         return pos[0]+lx,pos[1]+ly
#     else:
#         return None

def flann_match(img,template,rect,threshold=0.7):
    lx, ly, rx, ry = rect
    rect_img = img[ly: ry, lx: rx]
    
    sift = cv2.xfeatures2d.SIFT_create()
    #sift = cv2.xfeatures2d.SURF_create()
    #sift = cv2.ORB_create()
    kp1, des1 = sift.detectAndCompute(template,None)
    kp2, des2 = sift.detectAndCompute(rect_img,None)

    index_params = dict(algorithm = 1, trees = 5)
    search_params = dict(checks = 50)
    #matcher=cv2.BFMatcher(normType=cv2.NORM_HAMMING,crossCheck=True)
    matcher=cv2.FlannBasedMatcher(index_params,search_params)
    matches = matcher.knnMatch(des1,des2,k=2)
    good=[]
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    point=m
    # cv2.imshow('img.png',rect_img)
    # cv2.imshow('template.png',template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # img3 = cv2.drawMatchesKnn(img1=template,keypoints1=kp2,img2=rect_img ,keypoints2=kp1, matches1to2=matches, outImg=rect_img, flags=2)
    # plt.imshow(img3),plt.show()
    # #           debug end
 
    if len(good)>0:
        point=good[0]

    if point:
        # 获取关键点的坐标
        # x,y = kp1[point.queryIdx].pt
        # cv2.rectangle(template, (int(x),int(y)), (int(x) + 5, int(y) + 5), (0, 255, 0), 2)
        # x,y=kp2[point.trainIdx].pt
        # cv2.rectangle(rect_img, (int(x),int(y)), (int(x) + 5, int(y) + 5), (0, 255, 0), 2)
        # cv2.imshow('a', template)
        # cv2.imshow('b', rect_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        x,y=kp2[point.trainIdx].pt
        #print(int(x)+lx,int(y)+ly)
        return int(x)+lx,int(y)+ly
    else:
        return None


class Device():
    
    
    #模拟器使用
    # d=u2.connect('127.0.0.1:7555')
    # _h,_w=d.window_size()
    #手机使用
    d=u2.connect('192.168.0.102:1989')
    _w,_h=d.window_size()

    _widthScale=1280/_w
    _heightScale=720/_h
    _wScale=_w/1280
    _hScale=_h/720
    img=None

    isLatest=False

    def __init__(self) -> None:
        self.img=self.screenShot()
        self.isLatest=True
        

    def screenShot(self):
        lock.acquire()
        tmpimg=self.d.screenshot()
        screen=cv2.cvtColor(np.array(tmpimg), cv2.COLOR_BGR2GRAY)
        size=screen.shape
        self.img = cv2.resize(screen,(int(size[1]*self._widthScale),int(size[0]*self._heightScale)),interpolation= cv2.INTER_LINEAR)
        # cv2.imshow('screen.png',self.img)
        # cv2.waitKey(0)
        self.isLatest=True
        lock.release()
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

    def findImg(self,event,threshold=0.8):
        event.Pos = matchRect(self.image(),
            event.Img,
            event.Rect,
            threshold)
        return event.Pos

    def find(self,event, threshold = 0.8):
        ##模板匹配
        # event.Pos = matchRect(self.image(),
        #     event.Img,
        #     event.Rect,
        #     threshold=threshold)
        # return event.Pos
        
        # #FLANN单应性匹配
        event.Pos= flann_match(self.image(),
            event.Img,
            event.Rect,
            0.7
        )
        return event.Pos

    def flush(self):
        if self.isLatest:
            return
        self.screenShot()
    
    def UseImg(self):
        self.isLatest=False

    def isCmpare(self,img1,img2):
        return match(img1,img2)


    

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
