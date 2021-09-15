import os

def run():
    dirpath = input("输入处理文件夹路径：").strip('\"')

    folderlist = os.listdir(dirpath)
    tmp = []
    for f in folderlist:
        if not os.path.isfile(os.path.join(dirpath,f)):
            tmp.append(f)
    folderlist = tmp.copy()

    for folder in folderlist:
        if len(os.listdir(os.path.join(dirpath,folder))) == 0:
            print(folder)


if __name__ == '__main__':
    run()