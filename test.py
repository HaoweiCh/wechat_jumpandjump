import os
import time
import math
import random

from PIL import Image, ImageTk

adb = '/usr/local/bin/adb'
path_img = '/Users/c/PycharmProjects/untitled/havaajump/screen.png'


def load_screenshot():
    while not os.system(f"{adb} shell screencap -p /sdcard/screenshot.png"):
        if os.system(f"{adb} pull /sdcard/screenshot.png {path_img}"):
            time.sleep(0.3)
        else:
            os.system(f"{adb} shell rm /sdcard/screenshot.png")
            break


def press_screen(t: int):
    p = ' '.join([str(random.choice(range(512, 1024))) for _ in range(4)])

    os.system(f"{adb} shell input touchscreen swipe {p} {t}")


from tkinter import Tk, PhotoImage, Label

top = Tk()
top.title('Demo')

point_start = ()


def click_event_callback(event):
    global point_start

    if point_start:
        print(f"ends at {(event.x,event.y)}")

        distance = math.sqrt((event.x - point_start[0]) ** 2 + (event.y - point_start[1]) ** 2)
        print(f'距离 {distance}')
        press_screen(int(distance * 2.19 * 2))
        time.sleep(0.8)

        load_screenshot()
        refresh()

        point_start = ()
    else:
        point_start = (event.x, event.y)
        print(f"starts at {point_start}")


label = Label(top)
label.bind("<Button-1>", click_event_callback)
img = None
label.pack()


def refresh():
    global img
    # 三倍缩图片
    img = Image.open(path_img)
    img = img.resize((int(n / 3) for n in img.size), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    label.configure(image=img)


load_screenshot()
refresh()
top.mainloop()
