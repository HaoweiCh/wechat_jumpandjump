import os
import time
import math
import random
from tkinter import Tk, PhotoImage, Label

import cv2
import numpy as np
from PIL import Image, ImageTk

PATH_IMG = '/Users/c/PycharmProjects/untitled/havaajump/screen.png'


###

class Base(object):

    def __init__(self):
        self.__img = None

        self.tk = Tk()
        self.tk.title('Demo')
        self.label = Label(self.tk)
        self.label.bind("<Button-1>", self.event_click_callback)
        self.label.pack()

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, i):
        self.__img = i
        self.tkimg = ImageTk.PhotoImage(i)
        self.label.configure(image=self.tkimg)

    def event_click_callback(self, event):
        """
        鼠标单击事件拦截

        :param event:
        :return:
        """

        if self.point_start:
            print(f"ends at {(event.x,event.y)}")

            distance = math.sqrt(
                (event.x - self.point_start[0]) ** 2 +
                (event.y - self.point_start[1]) ** 2)
            print(f'距离 {distance}')
            self.press_screen(int(distance * 2.19 * 2))
            time.sleep(1.2)

            self.point_start = ()
            self.refresh()
        else:
            point_start = (event.x, event.y)
            print(f"starts at {point_start}")

    def press_screen(self, t: int):
        raise NotImplemented

    def refresh(self):
        raise NotImplemented


class Jump(Base):
    def __init__(self, path_img, adb='adb'):
        self.adb = adb
        self.path_img = path_img

        super(Jump, self).__init__()

        self.point_start = ()

        self.refresh()
        self.tk.mainloop()

    def refresh(self):
        # 保证能从MIUI系统中读到关键信息
        while not os.system(f"{self.adb} shell screencap -p /sdcard/screenshot.png"):
            if os.system(f"{self.adb} pull /sdcard/screenshot.png {self.path_img}"):
                print('稍后重试')
                time.sleep(0.3)
            else:
                # os.system(f"{adb} shell rm /sdcard/screenshot.png")
                break

        img = Image.open(self.path_img)
        # 三倍缩图片
        self.img = img.resize((int(n / 3) for n in img.size), Image.ANTIALIAS).convert('RGB')
        self.__parse_start_point()

    def __parse_start_point(self):
        self.point_start = ()

        # transfor to opencv format
        img = np.array(self.img)[:, :, ::-1].copy()

        # 创建NumPy数组
        lower = np.array([65, 40, 45], dtype="uint8")  # 颜色下限
        upper = np.array([120, 65, 65], dtype="uint8")  # 颜色上限
        # 数值按[b,g,r]排布
        # 如果color中定义了几种颜色区间，都可以分割出来

        # 根据阈值找到对应颜色
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        cany = cv2.Canny(img, 50, 150)

        # cv2.imshow("images", cany)
        # cv2.waitKey(0)

        # 展示图片
        # cv2.imshow("images", np.hstack([img, output]))
        # cv2.waitKey(0)

        # cv2.imshow("images", output)
        # cv2.waitKey(0)

        # cv2.imshow("mask", mask)
        # cv2.waitKey(0)

        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 筛选面积小的
        for cnt in contours:
            # 计算该轮廓的面积
            area = cv2.contourArea(cnt)

            # 面积小的都筛选掉
            if (area < 500):
                continue

            # box是四个点的坐标
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.int0(box)

            # # 计算高和宽
            # height = abs(box[0][1] - box[2][1])
            # width = abs(box[0][0] - box[2][0])
            #
            # print(height * 3, width * 3)

            start = box[0]
            end = box[3]
            mid = int((end[0] - start[0]) / 2 + start[0]), int(start[1])

            # 给锁定区域上色
            # y1 y2 x1 x2
            # img[50:200, 0:200] = (0, 0, 255)
            img[mid[1] - 6:mid[1], mid[0] - 3:mid[0] + 3] = (0, 255, 0)
            self.img = Image.fromarray(img)

            self.point_start = mid

    def press_screen(self, t: int):
        p = ' '.join([str(random.choice(range(512, 1024))) for _ in range(4)])

        os.system(f"{self.adb} shell input touchscreen swipe {p} {t}")


# for p in [
#     'screen copy 3.png',
#     'screen copy 2.png',
#     'screen copy.png',
#     'screen.png'
# ]:
#     d = Jump(p)
#     print(d.point_start)
#     d.img.show()

if __name__ == '__main__':
    Jump(PATH_IMG)
