# -*- coding: utf-8 -*-
# @Time    : 8/10/2021 5:09 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : run.py.py
# @Software: PyCharm
# @Description:


import traceback
import os

features = {}
features_id = {}
features_description = {}


def register_feature(description="暂无描述"):
    def wrap(func):
        if func.__name__ not in features.keys():
            feature_name = func.__name__
            features[feature_name] = func
            features_description[feature_name] = description
        return func

    return wrap


def run_feature(func):
    print(f"运行功能：{func.__name__}")
    return func()


def show_description():
    for n, (k, v) in enumerate(features.items()):
        features_id[n] = k
        print(f'{n}: {k}')
        print(features_description[k])


@register_feature(description="""用于显示所有的功能
""")
def show_features():
    print('目前以下功能可用：')
    for n, (k, v) in enumerate(features.items()):
        features_id[n] = k
        print(f'{n}: {k}', end=' ')
        print(f"({features_description[k].splitlines()[0]})")


@register_feature(description="""用来修改A+图片尺寸的
""")
def image_resizer():
    from features.image_resizer import run
    run()


@register_feature(description="""用来修正文件类型的
""")
def filetype_corrector():
    from features.filetype_corrector import run
    run()


@register_feature(description="""用来批量重命名文件的
""")
def item_renamer():
    from features.item_renamer import run
    run()

@register_feature(description="""用来处理标题大写的
""")
def title_capitalize():
    from features.title_capitalizer import run
    run()


if __name__ == '__main__':
    try:
        show_features()
        opt = input("请输入要运行的功能编号（输入help查看完整功能描述）：")
        if opt == "help":
            show_description()
        elif opt.isalnum() and int(opt) < len(features):
            run_feature(features[features_id[int(opt)]])
        else:
            print("无法识别此功能。")
    except Exception as err:
        print(err)
        traceback.print_exc()
