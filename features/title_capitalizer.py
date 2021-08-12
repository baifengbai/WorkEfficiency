# -*- coding: utf-8 -*-
# @Time    : 8/12/2021 11:04 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : title_capitalizer.py
# @Software: PyCharm
# @Description:
import re
import pyperclip

available_lang = ['en', 'es','fr','de','it']

def capitalize(s,lang='en'):
    if lang not in available_lang:
        exit('unsupported language. ')

    with open(f'resource/word-list/{lang}.txt','r',encoding='UTF-8') as ignore_file:
        ignore_list = ignore_file.read().splitlines()

    sentence_group = s.split('\n')
    word_list = [sentence.split(' ') for sentence in sentence_group]
    remade_string = []
    for i in range(len(word_list)):
        for j in range(len(word_list[i])):
            pattern = r"[^.,()]+"
            try:
                raw_s = re.search(f'({pattern})', word_list[i][j])[1]
            except:
                raw_s = word_list[i][j]
            if j == 0:
                continue
            if raw_s.lower().startswith('d\''):
                continue
            if raw_s.lower() not in ignore_list:
                # print(f"{word_list[i][j]} to {word_list[i][j].capitalize()}")
                raw_s_new = raw_s.capitalize()
                result = re.sub(pattern, raw_s_new, word_list[i][j], count=1)
                word_list[i][j] = result
            else:
                word_list[i][j] = word_list[i][j].lower()
        temp_s = ' '.join(word_list[i])
        remade_string.append(temp_s)
    return '\n'.join(remade_string)


def run():
    content = []
    lang = input('选择目标语言(en/fr/de/es/it)：')
    if lang not in available_lang:
        exit(f'unsupported language: {lang}. ')

    line = input('请输入文本，按 Ctrl-D 完成输入确认：\n')
    content.append(line)
    while True:
        try:
            line = input()
        except EOFError:
            break
        content.append(line)
    s = '\n'.join(content)
    s = s.replace(b'\xc2\xa0'.decode('utf-8'),' ')
    print('输出结果：')
    result = capitalize(s,lang=lang)
    print(result)

    pyperclip.copy(result)
    print('\n')
    print('内容已复制到剪切板，程序结束。')