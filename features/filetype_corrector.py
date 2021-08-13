import os
import filetype


def filetype_correct(path):
    result = os.walk(path)
    for root, dirs, files in result:
        for f in files:
            flag = False
            fpath = os.path.join(root, f)
            fname, default_ext = os.path.splitext(f)
            default_ext = default_ext.strip('.')
            kind = filetype.guess(fpath)
            try:
                true_ext = kind.extension
                mime = kind.mime
                if ('image' in mime.split('/')[0]) and (default_ext != true_ext):
                    flag = True
            except:
                true_ext = default_ext

            if flag:
                os.rename(fpath, os.path.join(root, '.'.join([fname, true_ext])))
                print(f"successfully renamed {f} to {'.'.join([fname, true_ext])}. ")


def run():
    path = input("输入需要处理的文件夹：").strip('\"').strip()
    filetype_correct(path)
