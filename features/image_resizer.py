# -*- coding: utf-8 -*-
# @Time    : 7/13/2021 7:28 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : image_resizer.py.py
# @Software: PyCharm
# @Description:

import os
import shutil
from PIL import Image, ImageOps
from PIL.JpegImagePlugin import JpegImageFile


# 图像处理函数
def resize(im: JpegImageFile, size: tuple, fillcolor: tuple) -> JpegImageFile:
    # size[0] is height, size[1] is width
    (width, height) = size

    required_ratio = height / width
    im_width, im_height = im.size
    im_ratio = im_height / im_width
    # 太高了，需要加宽
    if im_ratio >= required_ratio:
        # 原图高度为最大限制
        resize_width, resize_height = int(height / im_ratio), height
        source_resized = im.resize((resize_width, resize_height))
        append_width_l = int((width - resize_width) / 2)
        append_width_r = width - resize_width - append_width_l
        # left, top, right, bottom = _border(border)
        im_dest = ImageOps.expand(
            source_resized,
            border=(append_width_l, 0, append_width_r, 0),
            fill=fillcolor)
    else:
        # 原图宽度为最大限制
        resize_width, resize_height = width, int(width * im_ratio)
        source_resized = im.resize((resize_width, resize_height))
        append_height_t = int((height - resize_height) / 2)
        append_height_b = height - resize_height - append_height_t
        im_dest = ImageOps.expand(
            source_resized,
            border=(0, append_height_t, 0, append_height_b),
            fill=fillcolor)

    return im_dest


# 路径规划函数
def prepare_path(root_path):
    # append_orignal = root_path.rstrip('\\').rstrip('/') + "-original"
    root_folder = os.path.basename(os.path.normpath(root_path))
    result_path = os.path.join(root_path, root_folder + '-result')

    def iter_folder(
            folder_path: str,
            full_folder_stack=None,
            full_file_stack=None,
            root_flag=False,
            size: tuple = None
    ) -> (list, list):
        if full_file_stack is None:
            full_file_stack = []
        if full_folder_stack is None:
            full_folder_stack = []

        if (root_flag == False) and (size is None):
            exit('root_flag or size parameter is missing.')
        item_list = os.listdir(folder_path)
        for i in item_list:
            subpath = os.path.join(folder_path, i)
            if os.path.isdir(subpath):
                if root_flag:
                    if i == root_folder + "-result":
                        continue
                    try:
                        s = i.split('x')
                        if len(s) != 2:
                            print(f"发现错误格式：{s}")
                        size = (int(s[0]), int(s[1]))
                    except:
                        print(f'文件夹尺寸格式错误: {i}，将跳过。')
                        continue
                full_folder_stack.append(subpath)
                full_folder_stack, full_file_stack = iter_folder(
                    subpath, full_folder_stack, full_file_stack, size=size)
            else:
                if root_flag:
                    pass
                else:
                    try:
                        size_ = size
                        full_file_stack.append((subpath, size_))
                    except:
                        exit("can't normally identify height and width. ")
        return full_folder_stack, full_file_stack

    full_folder_stack, full_file_stack = iter_folder(
        folder_path=root_path,
        root_flag=True,
        size=None)
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.mkdir(result_path)
    result_folder_stack = [(
                               lambda x: x.replace(root_path, result_path)
                           )(folder) for folder in full_folder_stack]
    # make result path
    for r in result_folder_stack:
        os.mkdir(path=str(r))

    for file in full_file_stack:
        try:
            with Image.open(file[0]) as im:
                resized = resize(im=im, size=file[1], fillcolor=(255, 255, 255))
                result_file_path = file[0].replace(root_path, result_path)
                resized.save(result_file_path, quality=100)
        except:
            pass


def run():
    root_path = input('请输入需要处理的文件夹：').strip('\"')
    root_path = root_path.rstrip('\\').rstrip('/')
    # 开始处理
    print('开始处理图片...')
    prepare_path(root_path=root_path)
    print('处理完成。')
