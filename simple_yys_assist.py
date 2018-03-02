import os
from PIL import Image
import time
import numpy as np
import random


Regions = {
    "接受邀请": (125, 240, 125+35, 240+35),
    "自动接受邀请": (219, 240, 219+35, 240+35),
    "战斗中": (469, 693, 469+8, 693+15),
    "战斗胜利": (440, 120, 440+40, 120+40),
    "战斗失败": (440, 120, 440+40, 120+40),
}

Assets = {
    "接受邀请": Image.open("assets/接受邀请.png"),
    "自动接受邀请": Image.open("assets/自动接受邀请.png"),
    "战斗中": Image.open("assets/战斗中.png"),
    "战斗胜利": Image.open("assets/战斗胜利.png"),
    "战斗失败": Image.open("assets/战斗失败.png")
}

Positions = {
    "接受邀请": (235, 261),
    "自动接受邀请": (144, 261),
    "战斗胜利": (555, 78),
    "战斗失败": (555, 78)
}


def check_scene(screenshot, scene_name):
    """ 检查当前的场景 """
    scene_region = Regions[scene_name]
    cropImg = np.array(screenshot.crop(scene_region))  # 裁剪区域
    scene_asset = np.array(Assets[scene_name])  # 获取指定
    return np.array_equal(scene_asset, cropImg)


def take_screenshot():
    """ 使用adb截图 """
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png > /dev/null")
    os.system("adb pull /sdcard/screenshot.png ./tmp.png")
    return Image.open("tmp.png")


def click_point(pos):
    """ 使用adb点击某处 """
    x = pos[0], y = pos[1]
    x = x + random.randint(-3, 3)  # 加入随机成分, 防止鬼使黑的检测把
    y = y + random.randint(-3, 3)
    os.system("adb shell input tap {x} {y}".format(x=x, y=y))


if __name__ == "__main__":
    last_scene = "无场景"  # 记录上次所在的场景
    now_scene = "无场景"  # 记录当前所在的场景

    victor_times = 0   # 记录战斗胜利的次数
    failing_times = 0  # 记录战斗失败的次数
    print("开始运行, 当前场景: 无场景")

    while True:
        screenshot = take_screenshot()
        if check_scene(screenshot, "接受邀请"):
            now_scene = "接受邀请"
            if check_scene(screenshot, "自动接受邀请"):
                now_scene = "自动接受邀请"
        elif check_scene(screenshot, "战斗中"):
            now_scene = "战斗中"
        elif check_scene(screenshot, "战斗胜利"):
            now_scene = "战斗胜利"
        elif check_scene(screenshot, "战斗失败"):
            now_scene = "战斗失败"
        else:
            now_scene = "无场景"

        if now_scene != last_scene:  # 如果场景变化了.
            print("场景切换到:", now_scene)

            if now_scene != "无场景" \
                    and now_scene != "战斗中" \
                    and now_scene != "组队中":
                click_point(Positions[now_scene])

            if now_scene == "战斗胜利":
                victor_times += 1
            elif now_scene == "战斗失败":
                failing_times += 1

            last_scene = now_scene  # 更新上次的场景

        time.sleep(0.1)
