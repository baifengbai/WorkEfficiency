import os
import shutil
import typing

from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import filetype

import tempfile
import os

from pdf2image import convert_from_path

from PIL import Image
import pytesseract

from pyzbar.pyzbar import decode

import PyPDF2

import pandas as pd


def _read_pdf():
    fpath = input('请输入文件路径：').strip('\"')
    with open(fpath, 'rb') as fp:
        pdfFileObject = fp
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject, strict=True)
        print(" No. Of Pages: ", pdfReader.numPages)
        pageObject = pdfReader.getPage(0)
        return pageObject.extractText()


def _read_bartag(fpath):
    kind = filetype.guess(fpath)
    img = typing.Any
    if kind.extension == "pdf":
        images_from_path = convert_from_path(fpath, dpi=600)
        for im in images_from_path:
            img = im
            break
    elif kind.extension in ['png', 'jpg', 'jpeg']:
        img = Image.open(fpath)
    else:
        exit('Unsupported file type. ')
    detectedBarcodes = decode(img)
    # If not detected then print the message
    barcode_ = []
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
        # Traveres through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # # Locate the barcode position in image
            # (x, y, w, h) = barcode.rect
            #
            # # Put the rectangle in image using
            # # cv2 to heighlight the barcode
            # cv2.rectangle(img, (x - 10, y - 10),
            #               (x + w + 10, y + h + 10),
            #               (255, 0, 0), 2)
            if barcode.data != "":
                # Print the barcode data
                barcode_.append(barcode.data.decode('ascii'))
                # print(barcode.type)
    s1 = pytesseract.image_to_string(img).strip()
    while True:
        s1 = s1.replace('\n\n', '\n')
        if "\n\n" not in s1:
            break
    ss = s1.splitlines()
    return barcode_, ss


def pdf_save2img():
    f_path = input('请输入处理文件夹：').strip('\"')
    result_path = input('请输入结果保存位置：').strip('\"')

    temp_file_list = os.listdir(f_path)
    file_list = []

    for file in temp_file_list:
        if ".pdf" in file:
            file_list.append(file)
    cot = len(file_list)
    print(f'You have {cot} pdf file(s).')
    n = 0
    for ff in file_list:
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(os.path.join(f_path, ff), dpi=600, output_folder=path)

            name, extension = os.path.splitext(ff)

        for im in images_from_path:
            im.save(os.path.join(result_path, name + ".jpg"))
        n += 1
        print(f"finished {n} in {cot}.")

# excel 添加条码
def add_tag():
    save_fpath = input("请输入文件路径：").strip('\"')
    thumb_img_path = input('请输入图片文件夹：').strip('\"')
    wb = load_workbook(save_fpath)
    ws = wb.active
    # ws['A1'].value = "sku"
    # ws['A1'].alignment = Alignment(horizontal='center')
    # ws['A1'].font = Font(bold=True)
    # set font

    # 生成表头名称字典
    col_names = {}
    current = 1
    for col in ws.iter_cols(1, ws.max_column):
        col_names[col[0].value] = get_column_letter(current)
        current += 1

    # 设定字体
    for col in ws.columns:
        for cell in col:
            cell.font = Font(name="Calibri")

    # 文本居中
    # for col in ws.columns:
    #     for cell in col:
    #         cell.alignment = Alignment(wrap_text=True, vertical='center')

    # 设定列表宽度
    col_width = 36
    ws.column_dimensions[col_names['tag']].width = col_width  # img

    # 添加图片
    sku_list = ws[col_names['sku']]
    lensku = len(sku_list)
    for x in range(1, lensku):
        sku = sku_list[x].value
        if os.path.exists(os.path.join(thumb_img_path, sku + '.jpg')):
            img = Image(os.path.join(thumb_img_path, sku + '.jpg'))
        else:
            continue
        width = img.width
        height = img.height
        img.width = min(max(width * 0.45, col_width * 7), col_width * 7)
        img.height = img.width / width * height
        ws.row_dimensions[x + 1].height = col_width * height / width * 6
        img.anchor = f'B{x + 1}'
        ws.add_image(img)

    wb.save(save_fpath)

# 验证fnsku与sku对应关系
def verify_bar():
    vfilepath = input('请输入验证表格文件路径：').strip('\"') # 必须含有sku和fnsku
    bardirpath = input('请输入条码文件夹路径：').strip('\"')
    vdf = pd.read_excel(vfilepath)
    vdf.columns = vdf.columns.str.lower()
    bar_list = os.listdir(bardirpath)
    bar_list_full = [os.path.join(bardirpath, barfile) for barfile in bar_list]
    print('识别条码数据...')
    count = 0
    lenf = len(bar_list_full)

    def _x(b,i,lenf):
        print(f'\r识别第{i}/{lenf}个文件.',end='')
        return _read_bartag(b)

    bar_data = [_x(b,n+1, lenf) for n,b in enumerate(bar_list_full)]
    print('\n开始数据验证...')
    flag = True
    for i in range(len(bar_list_full)):
        bc, s = bar_data[i]
        if (bc[0] in vdf['fnsku'].values) and (vdf.loc[vdf['fnsku'] == bc[0]]['sku'].iloc[0] in ' '.join(s)):
            pass
        else:
            name, ext = os.path.splitext(bar_list[i])
            print(f'数据不匹配: {bar_list[i]}')
            if flag:
                os.mkdir(os.path.join(bardirpath,'unmatch'))
            os.rename(bar_list_full[i], os.path.join(bardirpath,'unmatch',name + ext))
            flag = False
    if flag:
        print('所有条码数据正确。')
    else:
        print('错误条码已标注，请修正。')

#barcode renamer,文件名修改为条码数据
def bar_info(mode='print'):
    if mode not in ['print','rename']:
        exit(f'模式不支持：{mode}')

    path = input("输入识别文件夹路径：").strip('\"')
    fl = os.listdir(path)
    fl_tmp = []
    for f in fl:
        f_ = os.path.join(path,f)
        if os.path.isfile(f_) and filetype.guess(f_).extension == 'pdf':
            fl_tmp.append(f)
    fl = fl_tmp.copy()
    result_path = os.path.join(path, 'result')
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.mkdir(result_path)
    for f in fl:
        f_name = os.path.join(path,f)
        bc,s = _read_bartag(f_name)
        name,ext = os.path.splitext(f)
        first_code = bc[0]
        if mode == 'rename':
            print(first_code)
            shutil.copyfile(f_name,os.path.join(result_path,first_code+ext))
        elif mode == 'print':
            print(first_code)


if __name__ == '__main__':
    # add_tag()
    # read_pdf()
    # verify_bar()
    bar_info(mode='rename')