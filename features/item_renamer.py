import os
import csv
import argparse

# 生成文件夹列表
def gen_item_list(root_path,type):
    itemx_list = os.listdir(root_path)
    item_list = []
    item_name_list = []
    judge = None
    if type == "folder":
        judge = os.path.isdir
    elif type == "file":
        judge = os.path.isfile
    else:
        exit("missing augments. ")

    for i in itemx_list:
        subpath = os.path.join(root_path, i)
        if judge(subpath):
            item_list.append(subpath)
            item_name_list.append(i)
        else:
            pass

    return item_list,item_name_list


def rename_item_name(root_path:str, task:list):
    previous = task[0]
    after = task[1]
    
    previous_path = os.path.join(root_path,previous)
    after_path = os.path.join(root_path, after)
    try:
        os.rename(previous_path,after_path)
        print(f'{previous} is successfully renamed.')
    except:
        print('failed renaming.')


def run():
    arg_mode = False
    if arg_mode:
        parser = argparse.ArgumentParser()
        parser.add_argument('--type',default='folder')
        args = parser.parse_args()
        print('选择模式：'+args.type)
        type = args.type
    else:
        available_type:set = {'folder','file'}
        while True:
            type = input("选择类型(folder or file)： ") or 'folder'
            if type in available_type:
                break
            else:
                print("不支持的类型")
    root_path = input('输入需要重命名的文件夹：').strip()
    item_list,item_name_list = gen_item_list(root_path=root_path,type=type)
    # print(item_name_list)
    with open(os.path.join(root_path,'rename.csv'),'w',encoding='UTF-8-sig',newline='') as f:
        writer = csv.writer(f)
        for x in item_name_list:
            writer.writerow([x])

    p = input("请打开csv文件，添加新文件夹名，保存，然后回车")

    with open(os.path.join(root_path,'rename.csv'),'r',encoding='UTF-8-sig') as f:
        rename_list = csv.reader(f)
        for l in rename_list:
            rename_item_name(root_path=root_path,task=l)


