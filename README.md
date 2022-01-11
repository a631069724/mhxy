梦幻西游自动脚本


本软件只用于技术交流，禁止用于非法用途，所有人都可以使用本软件的任何部分或全部代码，但是如果发生法律纠纷，作者不承担任何连带责任，也禁止读者讲软件用于非法用途


学习使用！！
学习使用！！！
学习使用！！！
不得商用，转载请注明出处！！！
欢迎共同爱好的小伙伴加入。
本人小菜鸟一枚，希望大佬帮忙指正，能让我更好的提高水平。

开发中(基本功能)...

使用uiautomator2 对手机进行操作
使用opencv判断图像

图像识别采用FLANN单应性匹配，支持模拟器、手机，不受分辨率影响，缺点运行缓慢。
如果只是用模拟器可以使用模板匹配，速度快。
utils.py文件中


    def find(self,event, threshold = 0.7):
        ##模板匹配
        # event.Pos = matchRect(self.image(),
        #     event.Img,
        #     event.Rect,
        #     threshold=threshold)
        #return event.Pos
        
        #FLANN单应性匹配
        event.Pos= flann_match(self.image(),
            event.Img,
            event.Rect,
            threshold
        )
        return event.Pos

TODO: 

    增加界面

    使用FLANN单应性匹配，优化效率

    关闭共享仅个人使用
    
