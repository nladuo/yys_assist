import os
from PIL import Image
import time
import numpy as np


def check_same(screenshot, des_img, where):
    pass


def take_screenshot():
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png > /dev/null")
    os.system("adb pull /sdcard/screenshot.png ./tmp.png > /dev/null")
    return np.array(Image.open("tmp.png"))


def click_point(x, y):
    os.system("adb shell input tap {x} {y}".format(x=x, y=y))


if __name__ == "__main__":
    # take_screenshot()
    # click_point(420, 250)
    # time.sleep(2)
    im = take_screenshot()
    print(im)
