import os
import shutil
import time
import yaml
from threading import Thread

import numpy as np
from PIL import Image


def convert_format(src_img: str):
    """
    将非tif格式的影像转换为tif影像，并删除原先的影像
    :param src_img: 原始影像的路径
    :return:
    """
    img = Image.open(src_img)
    name = os.path.splitext(src_img)[0]
    dst_tif = name + '.tif'
    img.save(dst_tif, 'TIFF')
    img.close()
    # 删除原先的img
    if os.path.exists(src_img):
        os.remove(src_img)


def gray_to_rgb(gray_img: str):
    """
    [0,255]的二值灰度影像设置调色板
    :param gray_img: [0,255]的二值灰度影像
    :return:
    """
    src = Image.open(gray_img)
    mat = np.array(src)
    dst = Image.fromarray(mat, 'P')
    bin_colormap = [0, 0, 0] + [255, 0, 0]  # 彩色调色板，以具体情况来定
    dst.putpalette(bin_colormap)
    # 保存
    rgb_img = gray_img
    name, suffix = os.path.splitext(gray_img)  # suffix 带.
    if '.png' != suffix:
        rgb_img = name + '.png'
    dst.save(rgb_img)
    src.close()


def create_sda(path: str, tile_size: int):
    sda_path = os.path.join(path, os.path.basename(path) + '.sda')
    shutil.copyfile('template.sda', sda_path)
    if os.path.exists(sda_path):
        with open(sda_path, 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        # 修改tile_size的值
        result['dataset']['tile_size'] = tile_size
        with open(sda_path, 'w') as f:
            yaml.dump(data=result, stream=f, allow_unicode=True, sort_keys=False)


def loop_convert_format(image_dir: str):
    """
    遍历指定的文件夹下的所有影像文件进行格式转换
    :param image_dir:
    :return:
    """
    for item in os.listdir(image_dir):
        src_img = os.path.join(image_dir, item)
        convert_format(src_img)


def loop_gray_to_rgb(image_dir: str):
    for item in os.listdir(image_dir):
        gray_img = os.path.join(image_dir, item)
        gray_to_rgb(gray_img)


def main(data_root: str):
    """
    普通串行的方式进行格式转换
    :param data_root:
    :return:
    """
    start = time.time()
    images = os.path.join(data_root, 'Images')
    masks = os.path.join(data_root, 'Masks')
    # 遍历影像数据转为tif
    loop_convert_format(images)
    # 遍历标签进行颜色转换
    loop_gray_to_rgb(masks)
    end = time.time()
    print("串行花费的时间：", end - start)
    # 创建sda文件
    img = Image.open(os.path.join(images, os.listdir(images)[0]))
    title_size = img.height
    img.close()
    create_sda(data_root, title_size)


def main_multi_thread(data_root: str):
    """
    开启多线程进行格式转换
    :param data_root:
    :return:
    """
    start = time.time()
    images = os.path.join(data_root, 'Images')
    masks = os.path.join(data_root, 'Masks')
    t1 = Thread(target=loop_convert_format, args=(images,))
    t3 = Thread(target=loop_gray_to_rgb, args=(masks,))
    # 启动线程
    t1.start()
    t3.start()
    # 等待所有线程执行完毕
    t1.join()
    t3.join()

    end = time.time()
    print("多线程执行花费的时间：", end - start)
    # 创建sda文件
    img = Image.open(os.path.join(images, os.listdir(images)[0]))
    title_size = img.height
    img.close()
    create_sda(data_root, title_size)


if __name__ == '__main__':
    data_root = 'data/DSIFN-Dataset'
    # main(data_root)
    main_multi_thread(data_root)
