# -*- coding: utf-8 -*-
# @Time    : 10/7/2021 10:39 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : date_parser.py
# @Software: PyCharm
# @Description:

import os
import re

import pandas as pd

def parse_date():
    file_path = input('输入表格路径：').strip('\"').strip('\\')
    result = os.walk(os.path.dirname(file_path))
    result2 = []
    sku_proj = None
    fdate_path = None
    subs_path = None
    flag_sku = True
    flag_fdate = True
    flag_subs = True
    for path,dirs,files in result:
        for file in files:
            _,ext = os.path.splitext(file)
            if ext.lower() in ['.csv']:
                result2.append((path,file))
            if flag_sku and (file == 'SKU-PROJECT.xlsx'):
                sku_proj = os.path.join(path,file)
                flag_sku = False
            if flag_fdate and (file == 'DATE-FORMAT.xlsx'):
                fdate_path = os.path.join(path,file)
                flag_fdate = False
            if flag_subs and (file == 'TYPE-MATCH.xlsx'):
                subs_path = os.path.join(path,file)
                flag_subs = False
    print('载入日期对应表。')
    fdate_df = pd.read_excel(fdate_path)
    fdate_list = [fdate_df[c].tolist() for c in fdate_df.columns]
    print('载入类型对应表。')
    subs_df = pd.read_excel(subs_path)
    subs_list = [subs_df[c].tolist() for c in subs_df.columns]

    print('读取表格...')
    df = pd.read_excel(file_path)
    print('完成数据读取。')
    count = 0
    lenall = len(df)
    print('开始分析...')
    for index,row in df.iterrows():
        print(f'\r分析：{index + 1} / {lenall}',end='')
        if '.' in row['date/time']:
            clist = re.findall('([0-9]+)\.([0-9]+)\.(.+)', row['date/time'])
            if len(clist) > 0 and len(clist[0]) == 3:
                clist_ = '/'.join([clist[0][1],clist[0][0],clist[0][2]])
                df.loc[index,'date/time'] = clist_
        for fdate in fdate_list:
            slice = row['date/time'].split(' ')
            if slice[1].lower() in fdate:
                df.loc[index, 'date/time'] = df.loc[index, 'date/time'].replace(slice[1].lower(), fdate[0])
                break
        for subs in subs_list:
            if row['type'] in subs:
                df.loc[index, 'type'] = df.loc[index, 'type'].replace(row['type'], subs[0])
    df['type'] = df['type'].str.lower()
    print('\n分析完成。')
    df['date/time'] = pd.to_datetime(df['date/time'])
    # Remove timezone from columns
    df['date/time'] = df['date/time'].dt.tz_localize(None)
    print('保存文件...')

    df.to_csv('result.csv',encoding='utf-8-sig')
    print('保存完成。')

if __name__ == '__main__':
    parse_date()