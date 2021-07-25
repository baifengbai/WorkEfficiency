# -*- coding: utf-8 -*-
# @Time    : 6/9/2021 12:07 AM
# @Author  : Chris.Wang
# @Site    : 
# @File    : run.py
# @Software: PyCharm
# @Description:


import tempfile
import os

from pdf2image import convert_from_path

if __name__ == '__main__':

    # find img path
    if not os.path.exists('img/'):
        os.mkdir('img')

    current_path = os.getcwd()
    temp_file_list = os.listdir(current_path)
    file_list = []

    for file in temp_file_list:
        if ".pdf" in file:
            file_list.append(file)
    cot = len(file_list)
    print(f'You have {cot} pdf file(s).')
    n = 0
    for ff in file_list:
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(ff, dpi=600, output_folder=path)

            name,extension = os.path.splitext(ff)

            for im in images_from_path:
                im.save("img/" + name + ".jpg")
            n += 1
            print(f"finished {n} in {cot}.")
    print('Done.')