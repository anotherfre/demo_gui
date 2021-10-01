import time
from PIL import ImageGrab
import cv2
import os
import random
import pyautogui as pg


os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})


def screen_shot(left, top, right, bot):
    # 截图
    bbox = (left, top, right, bot)
    img = ImageGrab.grab(bbox)
    img.save("jietu.png")
    img = cv2.imread("jietu.png", 0)
    os.remove("jietu.png")
    return img


def Template(template, left, top, right, bot):
    # 匹配
    img = screen_shot(left, top, right, bot)
    w, h = template.shape[::-1]
    method = eval("cv2.TM_SQDIFF_NORMED")
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bot_right = (top_left[0] + w, top_left[1] + h)
    point = min_val
    return top_left, bot_right, point  # 返回 匹配到的坐标、相似度


def myClick(top_left, bot_right, left, top):  # 点击图像的矩形坐标（top_left，bot_right） left为程序离桌面左边距离，top同理
    # 点击
    rand_x = random.randint(top_left[0], bot_right[0] - 20)  # -20为内调一点，不然会点击到边缘
    rand_y = random.randint(top_left[1], bot_right[1] - 20)
    pg.moveTo(left + rand_x, top + rand_y)
    pg.click(button='left')
    time.sleep(random.randint(1, 2))


def click_temp(temp, left, top, right, bot):
    template = cv2.imread(temp, 0)
    top_left, bot_right, point = Template(template, left, top, right, bot)
    if point < 0.05:
        myClick(top_left, bot_right, left, top)
    return point


if __name__ == '__main__':
    myClick([100, 100], [200, 200], 100, 100)
