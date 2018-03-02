""" 裁剪图片资源,用于识别 """
from PIL import Image
import numpy as np
from simple_yys_assist import Regions, Assets


def crop_screenshot(img_file, pos_x, pos_y, width, height, out_file):
    img = Image.open(img_file)
    region = (pos_x, pos_y, pos_x + width, pos_y + height)
    cropImg = img.crop(region)
    cropImg.save(out_file)
    print("exported:", out_file)


def check_scene(img_file, scene_name):
    """ 检查当前的场景 """
    img = Image.open(img_file)

    scene_region = Regions[scene_name]
    cropImg = np.array(img.crop(scene_region))  # 裁剪区域

    scene_asset = np.array(Assets[scene_name])  # 获取指定

    result = np.array_equal(scene_asset, cropImg)

    print("checked %s is %s ----> %s" % (img_file, scene_name, result))
    return result


if __name__ == "__main__":
    # 导出资源
    crop_screenshot("raw/接受邀请.png", 125, 240, 35, 35, "assets/接受邀请.png")
    crop_screenshot("raw/自动接受邀请.png", 219, 240, 35, 35, "assets/自动接受邀请.png")
    crop_screenshot("raw/战斗中.png", 1130, 58, 15, 15, "assets/战斗中.png")
    crop_screenshot("raw/战斗胜利.png", 440, 120, 40, 40, "assets/战斗胜利.png")
    crop_screenshot("raw/战斗失败.png", 440, 120, 40, 40, "assets/战斗失败.png")

    # 检查是否正确
    check_scene("raw/战斗胜利.png", "战斗失败")
    check_scene("raw/战斗胜利.png", "战斗胜利")
    check_scene("raw/自动接受邀请.png", "接受邀请")
    check_scene("raw/自动接受邀请.png", "自动接受邀请")

